from django.shortcuts import render, get_object_or_404, redirect
from .models import PlanFactTab
# import datetime
from django.core.paginator import Paginator

import logging

import openpyxl
from io import BytesIO
from django.http import HttpResponse
from openpyxl.styles import PatternFill, Alignment, Font, Border, Side

# ------------------------------------------------- Зона логгирования ----------------
class MyFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('GET') and not record.getMessage().startswith('POST')

# Создайте логгер
logger = logging.getLogger(__name__)

# Установите уровень логирования
logger.setLevel(logging.INFO)

# Создайте обработчик логирования для файла
file_handler = logging.FileHandler('log_plf.txt')
# Установите формат логирования
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(name)s -  %(message)s')
# file_handler.setFormatter(formatter)
# Добавьте фильтр логирования к обработчику логирования
file_handler.addFilter(MyFilter())

# Добавьте обработчик логирования к логгеру
logger.addHandler(file_handler)

# -------------------------------------------------  логгирования -----------------------

def plf_start_list(request):
    # --------------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # groups = Group.objects.all()
    print(user_groups_list)

    # --------------

    is_vps_group = request.user.groups.filter(name='vps').exists()
    query_fio = request.GET.get('search_fio', '')  # Получаем строку поиска по FIO
    query_kurir = request.GET.get('search_kurir', '')  # Получаем строку поиска по курирующему подразделению
    query_otrabot = request.GET.get('search_otrabot', '')  # Получаем строку поиска по отработанным записям
    query_data_zamecaniya = request.GET.get('search_data_zamecaniya', '')  # Получаем строку поиска по отработанным записям
    records_per_page = request.GET.get('records_per_page', 20)  # Получаем количество записей на странице
    print(query_data_zamecaniya)
    # Фильтруем данные по обоим полям и сортируем по p_p
    # data_smp = SmpRazborTab.objects.all().order_by('p_p')  # Сортировка по возрастанию p_p
    # Фильтруем данные по обоим полям
    print(request.user.groups)

    if user_groups_list == ['vps']:   # ------------------------- ВКЛЮЧИТЬ визмость ОТПРАВКИ В КЭР
    # if user_groups_list == ['#']:     # ------------------------- отключить визмость ОТПРАВКИ В КЭР
        # Исключаем записи, у которых ok_vps равно "ВПС"
        data_plf = PlanFactTab.objects.filter(ok_status_zapolnenia="Заполняется ВПС").order_by('data_planfakta',
                                                                                  'fio_pacienta')  # Сортировка по возрастанию
    else:
        data_plf = PlanFactTab.objects.all().order_by('data_planfakta', 'fio_pacienta')  # Сортировка по возрастанию
    total_records = data_plf.count()  # Общее количество записей

    if query_fio:
        data_plf = data_plf.filter(fio_pacienta__icontains=query_fio)

    if query_kurir:
        data_plf = data_plf.filter(ovpp_name__icontains=query_kurir)

    if query_otrabot:
        data_plf = data_plf.filter(ok_status_zapolnenia=query_otrabot)

    if query_data_zamecaniya:
        data_plf = data_plf.filter(data_planfakta=query_data_zamecaniya)


    # data_smp = data_smp.filter(ok_vps=query_kurir)
    # Получаем уникальные значения для выпадающего списка
    unique_kurir = PlanFactTab.objects.values_list('ovpp_name', flat=True).distinct()
    unique_otrab = PlanFactTab.objects.values_list('ok_status_zapolnenia', flat=True).distinct()

    paginator = Paginator(data_plf, records_per_page)  # Показывать 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter_records = data_plf.count()
    return render(request, 'planfact_home_page.html', {
        'data_plf': page_obj,
        'paginator':paginator,
        'search_fio': query_fio,
        'search_kurir': query_kurir,
        'search_otrabot': query_otrabot,
        'records_per_page': records_per_page,
        'total_records': total_records,  # Передаем общее количество записей
        'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст по курир. филиалу ВПС
        'unique_otrab': unique_otrab,  # Передаем уникальные значения в контекст по отработанным в КЭР
         'search_data_zamecaniya': query_data_zamecaniya,  # Передаем уникальные значения в контекст по отработанным в КЭР

        'groups': user_groups_list, # Получаем все группы
        'filter_records': filter_records,  ## количество записей - отфильтрованное
    })


def plf_edit_patient(request, id):
    # -------------- группу передадим ---
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # --------------

    patient = get_object_or_404(PlanFactTab, id=id)

    # --------------- вычсление перес=менных по ДНЯМ!!! ------------
    if request.method == 'POST':
        # ---------   Заполняем поля, которые НУЖНО считать со страницы и сохранять ------------

        logger.info(f'пользователь {request.user} вошел к пациенту {patient.fio_pacienta} -- {patient.data_planfakta}')
        patient.otvet_kc = request.POST.get('otvet_kc')
        patient.defekty_v_okazanii_pmp_na_osnovanii_karty_kontrolya_kachest = request.POST.get('defekty_v_okazanii_pmp_na_osnovanii_karty_kontrolya_kachest')
        patient.opisanie_defektov = request.POST.get('opisanie_defektov')
        patient.vyvody_svyaz_perenosa_vizita_s_defektami_okazaniya_pmp = request.POST.get('vyvody_svyaz_perenosa_vizita_s_defektami_okazaniya_pmp')
        patient.vypolnennye_meropriyatiya_po_nedopushcheniyu_perenosov = request.POST.get('vypolnennye_meropriyatiya_po_nedopushcheniyu_perenosov')

        # --------------------Проверяем ДАТУ !!!!--------------------------------------------------
        # patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc = zamena_pustot(
        #                                                         patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc)

        # -----------------------
        # print('1проверка кнопки -----------------')
        if 'plf_save_vps' in request.POST:  # Кнопка "Сохранить"
            print('109-----------------')
            logger.info(
                f'пользователь {request.user} сохранил инф-ю о {patient.fio_pacienta} -- {patient.data_planfakta}')
            patient.save()
            return redirect('app_planfact:plf_start_list')

        elif 'ot_ker_nazad_v_vps' in request.POST:  # Кнопка "назад на ВПС"
            patient.ok_status_zapolnenia = "Заполняется ВПС"
            patient.save()
            return redirect('app_planfact:plf_start_list')  # Возвращаем на страницу редактирования


        elif 'plf_send_to_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            # patient.ok_status_zapolnenia = "Передано в КЭР"

            patient.save()  # Сохраняем изменения
            return redirect('app_planfact:plf_proverka_to_ker', id=patient.id)  # Переходим на страницу проверки



    return render(request, 'plf_edit_pac_short.html', {'patient': patient,
                                                       'groups': user_groups_list,  # Получаем все группы

                                                       })
def plf_proverka_to_ker(request, id):
    patient = get_object_or_404(PlanFactTab, id=id)

    if request.method == 'POST':
        if 'ot_vps_v_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_status_zapolnenia = "Передано в КЭР"
            logger.info(
                f'пользователь {request.user} отправил запись о {patient.fio_pacienta} -- {patient.data_planfakta} в КЭР')
            patient.save()
            return redirect('app_planfact:plf_start_list')  # Переходим на главную страницу

        elif 'korrektirovat' in request.POST:  # Кнопка "Корректировать"
            return redirect('app_planfact:plf_edit_patient', id=id)  # Возвращаем на страницу редактирования

    return render(request, 'plf_patient_detail.html', {'patient': patient})


def plf_export_to_excel(request):
    # Получите данные с учетом фильтров
    search_data_zamecaniya = request.GET.get('search_data_zamecaniya', '')

    # Примените фильтры к вашему запросу
    data_plf = PlanFactTab.objects.all()  # Замените на ваш запрос
    if search_data_zamecaniya:
        data_plf = data_plf.filter(data_planfakta=search_data_zamecaniya)  # Замените на ваше поле

    # Создание Excel файла
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Patients Data'

    # Заголовки столбцов
    headers = [
        'Дата план-факта',
        'ОМС',    'ФИО',    'ДР',    'ОВПП',
        'Плановая дата визита согласно ЕМИАС/реестру',
        'Фактическая дата визита согласно ЕМИАС',
        'Вопрос для разбора',
        'Ответ КЦ'
    ]
    worksheet.append(headers)
    # Установка ширины для 2-го и 15-го столбца
    worksheet.column_dimensions['A'].width = 10  # Установите нужную ширину для 2-го столбца
    worksheet.column_dimensions['B'].width = 25  # Установите нужную ширину для 2-го столбца
    worksheet.column_dimensions['C'].width = 41  # Установите нужную ширину для 2-го столбца
    worksheet.column_dimensions['D'].width = 16  # Установите нужную ширину столбца
    worksheet.column_dimensions['E'].width = 39  # Установите нужную ширину  столбца
    worksheet.column_dimensions['F'].width = 25  # Установите нужную ширину  столбца
    worksheet.column_dimensions['G'].width = 20  # Установите нужную ширину  столбца
    worksheet.column_dimensions['H'].width = 42  # Установите нужную ширину  столбца
    worksheet.column_dimensions['I'].width = 47  # Установите нужную ширину  столбца

    # Форматирование заголовков
    blue_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')  # цвет
    yellou_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # цвет

    # Индексы заголовков, к которым нужно применить зеленый фон (начиная с 1)
    blue_header_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # Индексы для 'ФИО врача',....', 'Вывод'
    yellou_header_indices = [9]  # Индексы для '...'

    for col in blue_header_indices:
        worksheet.cell(row=1, column=col).fill = blue_fill  # Применяем зеленый фон к указанным заголовкам

    for col in yellou_header_indices:
        worksheet.cell(row=1, column=col).fill = yellou_fill  # Применяем зеленый фон к указанным заголовкам

    # Установка переноса текста для заголовков и жирного шрифта
    bold_font = Font(bold=True)  # Создаем объект шрифта с жирным начертанием

    # Создание границ
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for col in range(1, len(headers) + 1):
        cell = worksheet.cell(row=1, column=col)
        cell.alignment = Alignment(wrap_text=True, horizontal='center',
                                   vertical='center')  # Устанавливаем перенос текста
        cell.font = bold_font  # Устанавливаем жирный шрифт
        cell.border = thin_border  # Применяем границы к ячейке заголовка

        # Заполнение данными
    # Заполнение данными
    for item in data_plf:
        row_data = [
            item.data_planfakta.strftime("%d.%m.%Y") if item.data_planfakta else '',  # Форматируем дату
            item.polis_oms,
            item.fio_pacienta,
            item.data_rozhdeniya.strftime("%d.%m.%Y") if item.data_rozhdeniya else '',  # Форматируем дату
            item.ovpp_name,
            item.planovaya_data_vizita_soglasno_emias_reestru.strftime(
                "%d.%m.%Y") if item.planovaya_data_vizita_soglasno_emias_reestru else '',  # Форматируем дату
            item.fakticheskaya_data_vizita_soglasno_emias.strftime(
                "%d.%m.%Y") if item.fakticheskaya_data_vizita_soglasno_emias else '',  # Форматируем дату
            item.vopros_dlya_razbora,
            item.otvet_kc,
        ]

        # Добавляем данные в строку
        worksheet.append(row_data)

        # Применяем границы ко всем ячейкам в текущей строке
        current_row = worksheet.max_row  # Получаем номер последней строки
        for col in range(1, len(row_data) + 1):
            cell = worksheet.cell(row=current_row, column=col)
            cell.border = thin_border  # Применяем границы к ячейке


    # Сохранение файла в памяти
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # ----- Формирую название файла --------
    if search_data_zamecaniya:
        file = f'plan_fact_{search_data_zamecaniya}.xlsx'
    else:      file = 'plan_fact_all.xlsx'
    print(file)

    # Создание HTTP ответа
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{file}"'
    return response
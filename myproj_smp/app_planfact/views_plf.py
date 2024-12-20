from django.shortcuts import render, get_object_or_404, redirect
from .models import PlanFactTab
# import datetime
from django.core.paginator import Paginator

import openpyxl
from io import BytesIO
from openpyxl.styles import PatternFill
from django.http import HttpResponse
from openpyxl.styles import PatternFill, Alignment


def plf_start_list(request):

    # --------------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # --------------

    is_vps_group = request.user.groups.filter(name='vps').exists()
    query_fio = request.GET.get('search_fio', '')  # Получаем строку поиска по FIO
    query_kurir = request.GET.get('search_kurir', '')  # Получаем строку поиска по курирующему подразделению
    query_otrabot = request.GET.get('search_otrabot', '')  # Получаем строку поиска по отработанным записям
    query_data_zamecaniya = request.GET.get('search_data_zamecaniya', '')  # Получаем строку поиска по отработанным записям
    records_per_page = request.GET.get('records_per_page', 10)  # Получаем количество записей на странице
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
        'search_fio': query_fio,
        'search_kurir': query_kurir,
        'search_otrabot': query_otrabot,
        'search_data_zamecaniya': query_data_zamecaniya, # Передаем дату замечания

        'records_per_page': records_per_page,
        'total_records': total_records,  # Передаем общее количество записей
        'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст по курир. филиалу ВПС
        'unique_otrab': unique_otrab,  # Передаем уникальные значения в контекст по отработанным в КЭР

        'filter_records': filter_records, # Получаем все группы
        'groups': user_groups_list, # Получаем все группы
    })


def plf_edit_patient(request, id):
    patient = get_object_or_404(PlanFactTab, id=id)

    # --------------- вычсление перес=менных по ДНЯМ!!! ------------
    if request.method == 'POST':
        # ---------   Заполняем поля, которые НУЖНО считать со страницы и сохранять ------------


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
            patient.save()
            return redirect('app_planfact:plf_start_list')

        elif 'plf_send_to_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            # patient.ok_status_zapolnenia = "Передано в КЭР"
            patient.save()  # Сохраняем изменения
            return redirect('app_planfact:plf_proverka_to_ker', id=patient.id)  # Переходим на страницу проверки



    return render(request, 'plf_edit_pac_short.html', {'patient': patient,
                                                       # 'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       # 'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover': dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,

                                                       })
def plf_proverka_to_ker(request, id):
    patient = get_object_or_404(PlanFactTab, id=id)

    if request.method == 'POST':
        if 'ot_vps_v_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_status_zapolnenia = "Передано в КЭР"
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

    #------------------------------------ Форматирование заголовков-----------------------н
    # green_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')  # Зеленый цвет
    # # Индексы заголовков, к которым нужно применить зеленый фон (начиная с 1)
    # green_header_indices = [15, 16,  17, 18, 19]  # Индексы для 'ФИО врача', 'Сравнение...', 'Действия ЦПП', 'Контроль...', 'Вывод'
    # for col in green_header_indices:
    #     worksheet.cell(row=1, column=col).fill = green_fill  # Применяем зеленый фон к указанным заголовкам
    #------------------------------------ Форматирование заголовков-----------------------к


    # ---------------------------
    blue_fill = PatternFill(start_color='b1e4fa', end_color='00FF00', fill_type='solid')  # Ситний цвет
    yellow_fill = PatternFill(start_color='14fa70', end_color='00FF00', fill_type='solid')  # Ситний цвет
    # Индексы заголовков, к которым нужно применить зеленый фон (начиная с 1)
    # green_header_indices = [15, 16, 17, 18,
    #                         19]  # Индексы для 'ФИО врача', 'Сравнение...', 'Действия ЦПП', 'Контроль...', 'Вывод'
    blue_header_indices = [1, 2, 3, 4, 5,6,7,8,]  # Индексы для 'ФИО врача', 'Сравнение...', 'Действия ЦПП', 'Контроль...', 'Вывод'
    yellow_header_indices = [9,]  # Индексы для 'ФИО врача', 'Сравнение...', 'Действия ЦПП', 'Контроль...', 'Вывод'

    # ------------------- для колонок с синим цветом -------------
    for col in blue_header_indices:
        cell = worksheet.cell(row=1, column=col)
        cell.fill = blue_fill  # Применяем Ситний фон к заголовкам
        cell.alignment = Alignment(wrap_text=True)  # Включаем перенос текста

    for col in yellow_header_indices:
        cell = worksheet.cell(row=1, column=col)
        cell.fill = yellow_fill  # Применяем Ситний фон к заголовкам
        cell.alignment = Alignment(wrap_text=True)  # Включаем перенос текста

    # ------------------- для колонок с зелен цветом -------------
    # Настройка ширины колонок
    column_widths = [20, 15, 25, 15, 20, 30, 30, 25]  # Ширина для каждой колонки
    for i, width in enumerate(column_widths, start=1):
        worksheet.column_dimensions[worksheet.cell(row=1, column=i).column_letter].width = width

    # ---------------------------

    # Заполнение данными
    for item in data_plf:
        worksheet.append([
            item.data_planfakta.strftime("%d.%m.%Y") if item.data_planfakta else '',  # Форматируем дату
            item.polis_oms,
            item.fio_pacienta,
            item.data_rozhdeniya.strftime("%d.%m.%Y") if item.data_rozhdeniya else '',  # Форматируем дату
            item.ovpp_name,
            item.planovaya_data_vizita_soglasno_emias_reestru.strftime("%d.%m.%Y") if item.planovaya_data_vizita_soglasno_emias_reestru else '',  # Форматируем дату
            item.fakticheskaya_data_vizita_soglasno_emias.strftime("%d.%m.%Y") if item.fakticheskaya_data_vizita_soglasno_emias else '',  # Форматируем дату
            item.vopros_dlya_razbora,
            item.otvet_kc,
        ])

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
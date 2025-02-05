import logging
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import KisLong
from .models import KisChange
from .forms_kis import KisLongFilterForm
from django.utils import timezone
from django.contrib import messages

from django.core.paginator import Paginator
from datetime import datetime

class MyFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('GET') and not record.getMessage().startswith('POST')

# Создайте логгер
logger = logging.getLogger(__name__)

# Установите уровень логирования
logger.setLevel(logging.INFO)

# Создайте обработчик логирования для файла
file_handler = logging.FileHandler('log.txt')

# Установите формат логирования
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(name)s -  %(message)s')
file_handler.setFormatter(formatter)
# Добавьте фильтр логирования к обработчику логирования
file_handler.addFilter(MyFilter())

# Добавьте обработчик логирования к логгеру
logger.addHandler(file_handler)


def zamena_pustot(pole_proverki_daty):
    # Функция проверки является ли значение в поле ДАТЫ - пустым??? для ВСЕХ ДАТ проверку!!!!
    # Проверяем ДАТУ, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
    if pole_proverki_daty == "":
        pole_proverki_daty = None
    else:
        pole_proverki_daty = pole_proverki_daty
    return pole_proverki_daty

def calculate_koiko_dni():
    # Получаем сегодняшнюю дату
    # logger.info('Index page accessed')
    today = timezone.now().date()  # Используем timezone для получения текущей даты

    # Получаем всех пациентов из таблицы kis_long_tab
    patients = KisLong.objects.all()

    # Проходим по каждому пациенту и вычисляем разницу в днях
    for patient in patients:
        if patient.data_gospit:  # Проверяем, что дата госпитализации не пустая
            # Вычисляем разницу в днях
            if patient.data_vypiski:
                raschet_kd = (patient.data_vypiski - patient.data_gospit).days
            else:
                difference = today - patient.data_gospit
            patient.kojko_dni = difference.days  # Сохраняем результат в поле koiko_dni
            patient.save()  # Сохраняем изменения в базе данных

def run_calculate_koiko_dni(request):
    calculate_koiko_dni()  # Вызываем вашу функцию
    logger.info(f'пользователь {request.user} произвел пересчет койко-дней')
    messages.success(request, 'Расчет koiko dni успешно выполнен.')  # Сообщение об успехе
    return redirect('app_kis_long:v_kis_home')  # Перенаправляем обратно на страницу home_kis

def v_kis_home(request):
    logger.info(f'пользователь {request.user} зашел в модуль КИС {request.user.groups.all()}')
    # -------------- получаю принадлежность к группе -------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))

    logger.info(f'пользователь {request.user} зашел в модуль КИС ')

    total_records = KisLong.objects.all().count() # Получаем количество записей на странице

    # records_per_page = request.GET.get('records_per_page', 10)  # Получаем количество записей на странице
    records_per_page = request.GET.get('records_per_page', request.session.get('records_per_page', 10))  # Получаем количество записей на странице


    if request.method == 'GET':
        # ---------------------------- сброс фильтров в 0 --------------
        if 'reset' in request.GET:
            form_filtr1 = KisLongFilterForm()
        else:
            # ------------------------ код для предотвращения сброса фильтров при переходе между страниц ----нач

            if 'page' in request.GET:
                request.GET = request.GET.copy()
                for key in ['fio_pacienta', 'otdelenie', 'kojko_dni_min', 'kojko_dni_max', 'records_per_page']:
                    if key not in request.GET:
                        request.GET[key] = ''
                # Добавьте также сохранение фильтров в GET-запросе
                for key, value in request.GET.items():
                    if key not in ['page', 'records_per_page']:
                        request.GET[key] = value
            # ------------------------ код для предотвращения сброса фильтров при переходе между страниц ----кон
            form_filtr1 = KisLongFilterForm(request.GET or None)
            if 'records_per_page' in request.GET and request.GET['records_per_page'] != '':
                request.session['records_per_page'] = int(request.GET['records_per_page'])


        # ---------------------------- сброс фильтров в 0 --------------

        # ----------------------если соц.коорд, то передача в ШАБЛОН только записей с "передано_в_соц"--н
        if 'soc_koordinator' in user_groups_list and len(user_groups_list) == 1:
            patients = KisLong.objects.filter(status_zapisi='передано_в_соц')
        else: patients = KisLong.objects.all()
        # ----------------------если соц.коорд, то передача в ШАБЛОН только записей с "передано_в_соц"--н

        if form_filtr1.is_valid():
            fio_pacienta = form_filtr1.cleaned_data['fio_pacienta']
            otdelenie = form_filtr1.cleaned_data['otdelenie']
            kojko_dni_min = form_filtr1.cleaned_data['kojko_dni_min']
            kojko_dni_max = form_filtr1.cleaned_data['kojko_dni_max']

            if fio_pacienta:
                patients = patients.filter(fio_pacienta__icontains=fio_pacienta)
            if otdelenie:
                patients = patients.filter(otdelenie__icontains=otdelenie)

            if not kojko_dni_min:        kojko_dni_min = 1
            if not kojko_dni_max:        kojko_dni_max = 10000
            patients = patients.filter(kojko_dni__range=(kojko_dni_min, kojko_dni_max))

        paginator = Paginator(patients, records_per_page)  # Показывать 10 записей на странице
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # filter_records = patients.count()
        # Сохраняем количество записей на странице в GET-запросе
        if 'records_per_page' not in request.GET:
            request.GET = request.GET.copy()
            request.GET['records_per_page'] = records_per_page


    return render(request, 'kis_long_home.html',
                      {'patients': patients,
                       'groups': user_groups_list,  # Получаем все группы
                       'form': form_filtr1,
                       'paginator': paginator,
                       'records_per_page':records_per_page,
                       'page_obj':page_obj,
                       'total_records':total_records
                       },
                  )


def v_kis_pac_detail(request, id):
    # -------------- группу передадим ---
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # --------------

    patient = get_object_or_404(KisLong, id=id)  # Получаем запись по ID
    logger.info(f'пользователь {request.user} зашел в детали по пациенту {patient.fio_pacienta}')

    if 'btn_correct_kriter' in request.POST:  # Кнопка "Изменить критерии"
        logger.info(f'пользователь {request.user} нажал btn_correct_kriter и зашел в правки по kriter -  {patient.fio_pacienta}')
        return redirect('app_kis_long:v_kis_pravka_kriterij', id=patient.id)

    if 'btn_correct_zayavka' in request.POST:  # Кнопка "Изменить zayavka"
        logger.info(
            f'пользователь {request.user} нажал btn_correct_zayavka и зашел в правки по zayavkе -  {patient.fio_pacienta}')
        return redirect('app_kis_long:v_kis_pravka_zayavka', id=patient.id)

    return render(request, 'kis_pac_detail.html',
                                    {
                                        'patient': patient,
                                        'groups': user_groups_list,  # Получаем все группы
                                         })

def v_kis_pravka_kriterij(request, id):
    patient = get_object_or_404(KisLong, id=id)
    patient_changed = KisChange()

    # ------------------- Шаги по сохранению изменений ---------- н
    ppi_old = patient.ppi
    medic_kriterii_old = patient.medic_kriterii
    med_pokazaniya_old = patient.med_pokazaniya
    soc_kriterii_old = patient.soc_kriterii
    funkciional_kriterii_old = patient.funkciional_kriterii
    psikh_kriterii_old = patient.psikh_kriterii
    org_kriterii_old = patient.org_kriterii
    nalichie_zayavki_v_soc_sluzhbu_old = patient.nalichie_zayavki_v_soc_sluzhbu
    sostoyanie_zayavki_old = patient.sostoyanie_zayavki
    prichna_otsutstviya_zayavki_old = patient.prichna_otsutstviya_zayavki
    kommentarij_old = patient.kommentarij

    old_status = {
                'ppi' : ppi_old,
                'medic_kriterii' : medic_kriterii_old,
                'med_pokazaniya' : med_pokazaniya_old,
                'soc_kriterii' : soc_kriterii_old,
                'funkciional_kriterii' : funkciional_kriterii_old,
                'psikh_kriterii' : psikh_kriterii_old,
                'org_kriterii' : org_kriterii_old,
                'nalichie_zayavki_v_soc_sluzhbu' : nalichie_zayavki_v_soc_sluzhbu_old,
                'sostoyanie_zayavki' : sostoyanie_zayavki_old,
                'prichna_otsutstviya_zayavki' : prichna_otsutstviya_zayavki_old,
                'kommentarij' : kommentarij_old,
                }
    # ------------------- Шаги по сохранению изменений ---------- к

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------
        patient.ppi = request.POST.get('ppi')
        patient.medic_kriterii = request.POST.get('medic_kriterii')
        patient.med_pokazaniya = request.POST.get('med_pokazaniya')
        patient.soc_kriterii = request.POST.get('soc_kriterii')
        patient.funkciional_kriterii = request.POST.get('funkciional_kriterii')
        patient.psikh_kriterii = request.POST.get('psikh_kriterii')
        patient.org_kriterii = request.POST.get('org_kriterii')
        patient.nalichie_zayavki_v_soc_sluzhbu = request.POST.get('nalichie_zayavki_v_soc_sluzhbu')
        patient.sostoyanie_zayavki = request.POST.get('sostoyanie_zayavki')
        patient.prichna_otsutstviya_zayavki = request.POST.get('prichna_otsutstviya_zayavki')
        patient.kommentarij = request.POST.get('kommentarij')

        new_status = {
                    'ppi': patient.ppi,
                    'medic_kriterii': patient.medic_kriterii,
                    'med_pokazaniya': patient.med_pokazaniya,
                    'soc_kriterii': patient.soc_kriterii,
                    'funkciional_kriterii': patient.funkciional_kriterii,
                    'psikh_kriterii': patient.psikh_kriterii,
                    'org_kriterii': patient.org_kriterii,
                    'nalichie_zayavki_v_soc_sluzhbu': patient.nalichie_zayavki_v_soc_sluzhbu,
                    'sostoyanie_zayavki': patient.sostoyanie_zayavki,
                    'prichna_otsutstviya_zayavki': patient.prichna_otsutstviya_zayavki,
                    'kommentarij': patient.kommentarij,
                  }



    if 'btn_save_kriter' in request.POST:  # Кнопка "Сохранить"
        logger.info( f'пользователь {request.user} сохранил  правки по kriter -  {patient.fio_pacienta}')

        for key in old_status:
            # Сравниваем значения по ключам
            if old_status[key] != new_status[key]:
                # Если значения отличаются, создаем новый объект KisChange
                patient_changed = KisChange(   # Устанавливаем связь с объектом KisLong
                    id_pacienta=patient.id,  # Записываем название id пациента
                    fio_pacienta=patient.fio_pacienta,  # # Записываем название колонки
                    name_changed_colon=key,  # Записываем название колонки
                    data_old=old_status[key],  # Записываем старое значение
                    data_new=new_status[key],  # Записываем новое значение
                    time_changed=datetime.now(),  # Записываем новое значение
                    who_changed=request.user,  # Записываем новое значение
                )
                patient_changed.save()  # Сохраняем объект в базе данных
                patient.data_last_changed = datetime.now()
        patient.save()

        return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)

    elif 'btn_otmena_pravki_kriter' in request.POST:  # Кнопка "ОТМЕНИТЬ правки в критериях"
        logger.info(
            f'пользователь {request.user} отменил правки по kriter -  {patient.fio_pacienta}')
        return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'pravka_kriterij.html', {'patient': patient,
                                                    })



def v_kis_pravka_zayavka(request, id):
    patient = get_object_or_404(KisLong, id=id)

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------
        patient.tema_zayavki_pomosh_v_zhizneustrojstve = request.POST.get('tema_zayavki_pomosh_v_zhizneustrojstve')
        patient.nalichie_rodstvennikov = request.POST.get('nalichie_rodstvennikov')

        # Проверяем, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        # patient.data_peredachi_soc_koordinatoram_dtszn = request.POST.get('data_peredachi_soc_koordinatoram_dtszn')
        # patient.data_peredachi_soc_koordinatoram_dtszn = zamena_pustot(patient.data_peredachi_soc_koordinatoram_dtszn)

        # Проверяем, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        patient.data_peredachi_soc_koordinatoram_dtszn = request.POST.get(
            'data_peredachi_soc_koordinatoram_dtszn')
        patient.data_peredachi_soc_koordinatoram_dtszn = zamena_pustot(
            patient.data_peredachi_soc_koordinatoram_dtszn)

        patient.fio_zaveduyushchego_otd = request.POST.get('fio_zaveduyushchego_otd')
        patient.fio_lechashchego_vracha = request.POST.get('fio_lechashchego_vracha')
        patient.kommentarij_soc = request.POST.get('kommentarij_soc')

        # Проверяем, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = request.POST.get('data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn')
        patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = zamena_pustot(patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn)

        patient.status_pacienta = request.POST.get('status_pacienta')
        patient.soc_koordinator = request.POST.get('soc_koordinator')
        patient.kommentarij_soc_koordinatorov_dtszn = request.POST.get('kommentarij_soc_koordinatorov_dtszn')
        patient.reshenie_po_pacientu = request.POST.get('reshenie_po_pacientu')

        # Проверяем, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        patient.data_prinyatiya_resheniya_po_pacientu = request.POST.get('data_prinyatiya_resheniya_po_pacientu')
        patient.data_prinyatiya_resheniya_po_pacientu = zamena_pustot(
            patient.data_prinyatiya_resheniya_po_pacientu)

        patient.pacient_ne_mozhet_vyrazit_svoe_soglasie = request.POST.get('pacient_ne_mozhet_vyrazit_svoe_soglasie')
        patient.otkaz_rodstvennikov = request.POST.get('otkaz_rodstvennikov')


        if 'btn_save_pravki_zayavka' in request.POST:  # Кнопка "Сохранить"
            patient.save()
            return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)

        elif 'btn_otmena_pravki_zayavka' in request.POST:  # Кнопка "ОТМЕНИТЬ правки в критериях"
            return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'pravka_zayavka.html', {'patient': patient, })


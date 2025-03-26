import logging
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import KisLong, KisChange, Kis
from .forms_kis import KisLongFilterForm
from .forms_kis import KisFilterForm
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.db.models.functions import Lower


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

def v_statistica(request):
    return render(request, 'kis_statistica.html')

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
                difference = (patient.data_vypiski - patient.data_gospit)
            else:
                difference = today - patient.data_gospit
            patient.kojko_dni = difference.days  # Сохраняем результат в поле koiko_dni
            patient.save()  # Сохраняем изменения в базе данных

def run_calculate_koiko_dni(request):
    calculate_koiko_dni()  # Вызываем вашу функцию
    logger.info(f'пользователь {request.user} произвел пересчет койко-дней')
    messages.success(request, 'Расчет koiko dni успешно выполнен.')  # Сообщение об успехе
    return redirect('app_kis_long:v_kis_home')  # Перенаправляем обратно на страницу home_kis

def v_find_new_in_kis(request):

    logger.info(f'пользователь {request.user} зашел в модуль КИС')
    # -------------- получаю принадлежность к группе -------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))

    # ------------------------ Получаем количество записей на странице
    records_per_page = request.GET.get('records_per_page', request.session.get('records_per_page', 10))  # Получаем количество записей на странице

    # Получаем текущую дату
    today = timezone.now().date()
    kojko_dni_min = (today - timezone.timedelta(days=60))  # - тут определяем ПОРОГ поиска долгих пациентов (койкодни)

    patients_all = Kis.objects.filter(
                        data_vipiski__isnull=True,
                        data_gospit__lt=kojko_dni_min,  # --- сколько к-дней берем в срез
                        ).exclude(
                                Q(otdelenie_name__icontains="респираторной поддержки") |
                                Q(otdelenie_name__icontains="помощи детям")
                            )

    if request.method == 'GET':
        # ---------------------------- сброс фильтров в 0 --------------
        if 'reset' in request.GET:
            form_filtr_kis = KisFilterForm()
        else:
            # ------------------------ код для предотвращения сброса фильтров при переходе между страниц ----нач
            if 'page' in request.GET:
                request.GET = request.GET.copy()
                for key in ['fio_pacienta', 'otdelenie', 'kojko_dni_min', 'kojko_dni_max', 'records_per_page']:
                    if key not in request.GET:
                        request.GET[key] = ''
                # Добавляем также сохранение фильтров в GET-запросе
                for key, value in request.GET.items():
                    if key not in ['page', 'records_per_page']:
                        request.GET[key] = value

            # ------------------------ код для предотвращения сброса фильтров при переходе между страниц ----кон

            form_filtr_kis = KisFilterForm(request.GET or None)
            if 'records_per_page' in request.GET and request.GET['records_per_page'] != '':
                request.session['records_per_page'] = int(request.GET['records_per_page'])


        if form_filtr_kis.is_valid():

            patients_all = Kis.objects.filter(data_vipiski__isnull=True,)

            filtr_pacient = form_filtr_kis.cleaned_data['form_fio_pacienta']
            filtr_otdelenie_name = form_filtr_kis.cleaned_data['form_otdelenie']
            filtr_kojko_dni_min = form_filtr_kis.cleaned_data['form_kojko_dni_min']

            if filtr_pacient:
                patients_all = patients_all.filter(pacient__icontains=filtr_pacient)
            if filtr_otdelenie_name:
                patients_all = patients_all.filter(otdelenie_name__icontains=filtr_otdelenie_name)

            # Применение фильтра по количеству дней
            if filtr_kojko_dni_min:
                kojko_dni_min = (today - timezone.timedelta(days=filtr_kojko_dni_min))
                patients_all = patients_all.filter(data_gospit__lt=(kojko_dni_min))
            else: kojko_dni_min = (today - timezone.timedelta(days=0))


            # ---------- Получили отфильрованных пациентов
            patients_all = patients_all.filter(data_gospit__lt=(kojko_dni_min))

        # Создаем список пациентов из KisLong для сравнения, приводя к нижнему регистру
        patients_in_kis_long = KisLong.objects.annotate(
                                                        fio_pacienta_lower=Lower('fio_pacienta'),
                                                        data_rozhdeniya_lower=Lower('data_rozhdeniya')
                                                        ).values_list('fio_pacienta_lower')

        # Фильтруем пациентов из Kis, которые отсутствуют в KisLong
        patients_not_in_kis_long = patients_all.exclude(
            Q(pacient__in=[p[0].lower() for p in patients_in_kis_long])
                                                       )
        total_new_pac = patients_not_in_kis_long.count()

        paginator = Paginator(patients_not_in_kis_long, records_per_page)  # Показывать 10 записей на странице
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Сохраняем количество записей на странице в GET-запросе
        if 'records_per_page' not in request.GET:
            request.GET = request.GET.copy()
            request.GET['records_per_page'] = records_per_page


    return render(request, 'kis_start.html',
                      {'patients': patients_all,
                       'groups': user_groups_list,  # Получаем все группы
                       'form': form_filtr_kis,
                       'paginator': paginator,
                       'records_per_page':records_per_page,
                       'page_obj':page_obj,
                       'total_new_pac':total_new_pac,
                       'today':today,
                       # 'kojko_dni_min':kojko_dni_min,
                       'result_kojko_dni':(today - kojko_dni_min).days,
                       })


def v_kis_home(request):
    logger.info(f'пользователь {request.user} зашел в модуль КИС')
    # ------ авто рассчет койко-дней ----- при каждом открытии страницы - перерасчет
    calculate_koiko_dni()  # Вызываем  функцию перерасчета
    logger.info(f'пользователь {request.user} произвел пересчет койко-дней')
    messages.success(request, 'Расчет koiko dni успешно выполнен.')  # Сообщение об успехе

    # -------------- получаю принадлежность к группе -------н
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # -------------- получаю принадлежность к группе -------к

    # -- считывание настроек для сортировки колонок
    order_by = request.GET.get('order_by')
    order_type = request.GET.get('order_type')

    records_per_page = request.GET.get('records_per_page', request.session.get('records_per_page', 10))  # Получаем количество записей на странице

    if request.method == 'GET':
        # ---------------------------- сброс фильтров в 0 --------------н
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

        # ---------------------------- сброс фильтров в 0 --------------к
        if 'soc_koordinator' in user_groups_list and len(user_groups_list) == 1:
            print('---------------- soc_koordinator in user_groups_list')
            patients = KisLong.objects.filter(potrebnost_v_soc_koordinat='2. Есть потребность в соц.координаторе')
        else:
            # patients = KisLong.objects.all()
            patients = KisLong.objects.filter(iskhod_gospit='Пациент в стационаре')  # Фильтруйте пациентов по умолчанию

        # Пример обработки фильтров и сортировки
        if form_filtr1.is_valid():
            # Применение фильтров
            patients = KisLong.objects.all()  # Начинаем с полного списка
            fio_pacienta = form_filtr1.cleaned_data['form_fio_pacienta']
            otdelenie = form_filtr1.cleaned_data['form_otdelenie']
            iskhod_gospit = form_filtr1.cleaned_data['form_iskhod_gospit']
            kojko_dni_min = form_filtr1.cleaned_data['form_kojko_dni_min']
            med_pokazaniya = form_filtr1.cleaned_data['form_med_pokazaniya']
            potrebnost_v_soc = form_filtr1.cleaned_data['form_potrebnost_v_soc']

            if fio_pacienta:
                patients = patients.filter(fio_pacienta__icontains=fio_pacienta)
            if otdelenie:
                patients = patients.filter(otdelenie__icontains=otdelenie)
            if iskhod_gospit:
                patients = patients.filter(iskhod_gospit=iskhod_gospit)
            if med_pokazaniya:
                patients = patients.filter(med_pokazaniya=med_pokazaniya)
            if potrebnost_v_soc:
                patients = patients.filter(potrebnost_v_soc_koordinat=potrebnost_v_soc)

            if kojko_dni_min:
                patients = patients.filter(kojko_dni__gte=kojko_dni_min)

        # Применение сортировки
        if order_by and order_type:
            patients = patients.order_by(f"{'-' if order_type == 'desc' else ''}{order_by}")

            # ------------- сортировка по полям шапки ----- к --


        total_pac = patients.count()
        paginator = Paginator(patients, records_per_page)  # Показывать 10 записей на странице

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
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
                       'total_pac':total_pac
                       })

def v_kis_pac_detail(request, id):

    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))

    patient = get_object_or_404(KisLong, id=id)  # Получаем запись по ID
    logger.info(f'пользователь {request.user} зашел в детали по пациенту {patient.fio_pacienta}')

    # Беру последнюю дату изменения поля "status_resheniya_o_perevode" из Ретро-таблицы
    last_time_changed = KisChange.objects.filter(id_pacienta=id,
                                                 name_changed_colon__icontains='status_resheniya_o_perevode').order_by('-time_changed').first()
    if last_time_changed:
        status_last_date = last_time_changed.time_changed.split(" ")[0]
    else:
        status_last_date = "Статус не определен"


    if 'btn_correct_kriter' in request.POST:  # Кнопка "Изменить критерии"
        logger.info(f'пользователь {request.user} нажал btn_correct_kriter и зашел в правки по kriter -  {patient.fio_pacienta}')
        #  передам через сессию СТАТУС последний по состоянию заявки
        request.session['status_last_date'] = status_last_date

        return redirect('app_kis_long:v_kis_pravka_kriterij', id=patient.id)

    if 'btn_correct_zayavka' in request.POST:  # Кнопка "Изменить zayavka"
        logger.info(
            f'пользователь {request.user} нажал btn_correct_zayavka и зашел в правки по zayavkе -  {patient.fio_pacienta}')
        #  передам через сессию СТАТУС последний по состоянию заявки
        request.session['status_last_date'] = status_last_date
        return redirect('app_kis_long:v_kis_pravka_zayavka', id=patient.id)

    return render(request, 'kis_pac_detail.html', {
                                                    'patient': patient,
                                                    'status_last_date' :status_last_date,
                                                     'groups': user_groups_list,  # Получаем все группы
                                                })

def v_new_is_kis_v_kislong(request, id):

    patient = get_object_or_404(Kis, id=id)  # Получаем запись по ID
    logger.info(f'пользователь {request.user} добавляет в kis_long данные по пациенту {patient.pacient}')


    # ------ поля для передачи через сессию (из данных о паценте КИСа) --------
    fio_pacienta = patient.pacient
    data_rozhd = patient.data_rozhd
    otdelenie_name = patient.otdelenie_name
    data_gospit = patient.data_gospit
    ib_nomer = patient.ib_nomer + '-' + patient.ib_god[2:]+ '-C'



    # ------------получаю значения полей для передачи через сессию (из ФОРМЫ СБОРА ДАННЫХ со СТРАНЦЫ kis_new_pac.html) ---н

    if request.method == 'POST':

        fio_zaveduyushchego_otd = request.POST.get('fio_zaveduyushchego_otd')
        fio_lechashchego_vracha = request.POST.get('fio_lechashchego_vracha')

        ppi = request.POST.get('ppi')
        med_pokazaniya = request.POST.get('med_pokazaniya')
        dinamika_sostoyania = request.POST.get('dinamika_sostoyania')
        dvigatel_activnost = request.POST.get('dvigatel_activnost')
        status_nabludeniya = request.POST.get('status_nabludeniya')
        potrebnost_v_soc_koordinat = request.POST.get('potrebnost_v_soc_koordinat')
        status_med_karty = request.POST.get('status_med_karty')
        status_po_mse = request.POST.get('status_po_mse')
        pacient_ne_mozhet_vyrazit_svoe_soglasie = request.POST.get('pacient_ne_mozhet_vyrazit_svoe_soglasie')
        funkciional_kriterii = request.POST.get('funkciional_kriterii')
        kommentarij = request.POST.get('kommentarij')
        iskhod_gospit = request.POST.get('iskhod_gospit')
        n_istorii_bolezni = request.POST.get('ib_nomer')


    # ------------------- поля для передачи через сессию (из ФОРМЫ СБОРА ДАННЫХ со СТРАНЦЫ kis_new_pac.html) --к-

    if 'btn_check_befor_save_new' in request.POST:  # Кнопка "Сохранить"

        request.session['fio_pacienta'] = fio_pacienta
        request.session['data_rozhd'] = data_rozhd.strftime('%Y-%m-%d')
        request.session['otdelenie_name'] = otdelenie_name
        request.session['data_gospit'] = data_gospit.strftime('%Y-%m-%d')
        request.session['ib_nomer'] = ib_nomer

        # ------готовим для передачи через СЕССИИ ------------
        request.session['fio_zaveduyushchego_otd'] = fio_zaveduyushchego_otd
        request.session['fio_lechashchego_vracha'] = fio_lechashchego_vracha
        request.session['ppi'] = ppi
        request.session['med_pokazaniya'] = med_pokazaniya
        request.session['dinamika_sostoyania'] = dinamika_sostoyania
        request.session['dvigatel_activnost'] = dvigatel_activnost
        request.session['status_nabludeniya'] = status_nabludeniya
        request.session['potrebnost_v_soc_koordinat'] = potrebnost_v_soc_koordinat
        request.session['pacient_ne_mozhet_vyrazit_svoe_soglasie'] = pacient_ne_mozhet_vyrazit_svoe_soglasie

        request.session['status_med_karty'] = status_med_karty
        request.session['status_po_mse'] = status_po_mse
        # request.session['soc_kriterii'] = soc_kriterii
        request.session['funkciional_kriterii'] = funkciional_kriterii
        # request.session['psikh_kriterii'] = psikh_kriterii
        request.session['kommentarij'] = kommentarij
        request.session['iskhod_gospit'] = iskhod_gospit
        request.session['n_istorii_bolezni'] = ib_nomer


        return redirect('app_kis_long:v_kis_proverka_new', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'kis_new_pac.html', {   'patient': patient,
                                                    })


def v_kis_proverka_new(request, id):

    # ---------- получаю из v_new_is_kis_v_kislong через сессию -------
    fio_pacienta_session = request.session.get('fio_pacienta')
    data_rozhdeniya_session = request.session.get('data_rozhd')

    otdelenie_name = request.session.get('otdelenie_name')
    data_gospit = request.session.get('data_gospit')
    data_gospit_format_date = datetime.strptime(data_gospit, '%Y-%m-%d').date()
    ib_nomer = request.session.get('ib_nomer')

    # ---------- получаю из v_new_is_kis_v_kislong через сессию -------
    fio_zaveduyushchego_otd_session = request.session.get('fio_zaveduyushchego_otd')
    fio_lechashchego_vracha_session = request.session.get('fio_lechashchego_vracha')
    ppi_session                     = request.session.get('ppi')
    med_pokazaniya_session          = request.session.get('med_pokazaniya')
    dinamika_sostoyania_session     = request.session.get('dinamika_sostoyania')
    dvigatel_activnost_session      = request.session.get('dvigatel_activnost')
    status_nabludeniya_session      = request.session.get('status_nabludeniya')
    potrebnost_v_soc_koordinat_session = request.session.get('potrebnost_v_soc_koordinat')
    sposoben_virazit_soglasie_session = request.session.get('sposoben_virazit_soglasie')

    status_med_karty_session = request.session.get('status_med_karty')
    status_po_mse_session = request.session.get('status_po_mse')
    funkciional_kriterii_session = request.session.get('funkciional_kriterii')
    kommentarij_session = request.session.get('kommentarij')
    iskhod_gospit_session = request.session.get('iskhod_gospit')
    n_istorii_bolezni_session = request.session.get('n_istorii_bolezni')


    if potrebnost_v_soc_koordinat_session == '2. Есть потребность в соц.координаторе':
        nazvanie_knopki_save = 'Подать заявку на соц.координатора'
        status_zapisi = 'Заявка на соц.координатора ПОДГОТОВЛЕНА',
        data_peredachi_soc_koordinatoram_dtszn = timezone.now().date()

    else:
        nazvanie_knopki_save = 'Сохранить в БД "долгих" госпитализаций (БЕЗ ЗАЯВКИ на соц.)'
        status_zapisi = 'Заявка не оформлялась',
        data_peredachi_soc_koordinatoram_dtszn = None

    # data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = data_peredachi_soc_koordinatoram_dtszn

    data_peredachi_soc_koordinatoram_dtszn_session = data_peredachi_soc_koordinatoram_dtszn
    # data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn_session = data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn


    if request.method == 'POST':
        if 'vnosim_new_pac_v_bazy_kis_long' in request.POST:  # Кнопка "vnosim_v_bazy"

            # ---------- формируем список переменных для записи в kis_long_tab:-----------


            new_kis_long = KisLong(
                # n_istorii_bolezni=ib_nomer,
                fio_pacienta=fio_pacienta_session,
                otdelenie=otdelenie_name,
                kojko_dni=(timezone.now().date() - data_gospit_format_date).days ,

                fio_zaveduyushchego_otd=fio_zaveduyushchego_otd_session,
                fio_lechashchego_vracha=fio_lechashchego_vracha_session,
                ppi=ppi_session,

                dinamika_sostoyania= dinamika_sostoyania_session,
                dvigatel_activnost=dvigatel_activnost_session,
                potrebnost_v_soc_koordinat=potrebnost_v_soc_koordinat_session,
                sposoben_virazit_soglasie=sposoben_virazit_soglasie_session,
                status_med_karty=status_med_karty_session,
                status_po_mse=status_po_mse_session,
                status_nabludeniya=status_nabludeniya_session,
                med_pokazaniya=med_pokazaniya_session,
                funkciional_kriterii=funkciional_kriterii_session,
                kommentarij=kommentarij_session,
                iskhod_gospit='Пациент в стационаре',
                n_istorii_bolezni =n_istorii_bolezni_session,

                # status_zapisi=status_zapisi[0],
                data_rozhdeniya=data_rozhdeniya_session,
                data_gospit=data_gospit_format_date,
                data_peredachi_soc_koordinatoram_dtszn=data_peredachi_soc_koordinatoram_dtszn_session,
                # data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn=data_peredachi_soc_koordinatoram_dtszn_session,
                data_last_changed_med=timezone.now().date()

            )
            print('--------------------------------------------------------------')
            print(data_peredachi_soc_koordinatoram_dtszn_session)
            new_kis_long.save()

            return redirect('app_kis_long:v_kis_home')   # Переходим на главную страницу

        elif 'korrektirovat' in request.POST:  # Кнопка "Корректировать"
            return redirect('app_kis_long:v_new_is_kis_v_kislong', id=id)  # Возвращаем на страницу редактирования

    return render(request, 'kis_proverka_new_pac.html', {
                                                            'id': id,

                                                            'fio_pacienta': fio_pacienta_session,
                                                            'data_rozhdeniya': data_rozhdeniya_session,
                                                            'otdelenie_name': otdelenie_name,
                                                            'data_gospit': data_gospit,
                                                            'data_gospit_format_date': data_gospit_format_date,
                                                            'ib_nomer': ib_nomer,

                                                            'fio_zaveduyushchego_otd_session': fio_zaveduyushchego_otd_session,
                                                            'fio_lechashchego_vracha_session': fio_lechashchego_vracha_session,
                                                            'ppi_session': ppi_session,
                                                            'med_pokazaniya_session': med_pokazaniya_session,
                                                            'dinamika_sostoyania_session': dinamika_sostoyania_session,
                                                            'dvigatel_activnost_session': dvigatel_activnost_session,
                                                            'status_nabludeniya_session': status_nabludeniya_session,
                                                            'potrebnost_v_soc_koordinat_session': potrebnost_v_soc_koordinat_session,
                                                            'sposoben_virazit_soglasie_session': sposoben_virazit_soglasie_session,
                                                            'status_med_karty_session': status_med_karty_session,
                                                            'status_po_mse_session': status_po_mse_session,
                                                            # 'soc_kriterii_session': soc_kriterii_session,
                                                            'funkciional_kriterii_session': funkciional_kriterii_session,

                                                            'kommentarij_session': kommentarij_session,
                                                            'iskhod_gospit_session': iskhod_gospit_session,
                                                            'n_istorii_bolezni_session': n_istorii_bolezni_session,

                                                            'nazvanie_knopki_save': nazvanie_knopki_save,
                                                            'status_zapisi': status_zapisi[0],
                                                            'data_peredachi_soc_koordinatoram_dtszn': data_peredachi_soc_koordinatoram_dtszn_session,


                                                          })

def v_kis_pravka_kriterij(request, id):
    patient = get_object_or_404(KisLong, id=id)
    # ---------- получаю из v_kis_pac_detail через сессию -------
    status_last_date = request.session.get('status_last_date')

    # ------------------- Шаги по сохранению изменений ---------- н
    fio_zaveduyushchego_otd_old = patient.fio_zaveduyushchego_otd
    fio_lechashchego_vracha_old = patient.fio_lechashchego_vracha
    ppi_old = patient.ppi
    med_pokazaniya_old = patient.med_pokazaniya
    dinamika_sostoyania_old = patient.dinamika_sostoyania
    dvigatel_activnost_old = patient.dvigatel_activnost
    status_nabludeniya_old = patient.status_nabludeniya
    potrebnost_v_soc_koordinat_old = patient.potrebnost_v_soc_koordinat

    sposoben_virazit_soglasie_old = patient.sposoben_virazit_soglasie
    status_med_karty_old = patient.status_med_karty
    status_po_mse_old = patient.status_po_mse
    funkciional_kriterii_old = patient.funkciional_kriterii

    kommentarij_old = patient.kommentarij
    iskhod_gospit_old = patient.iskhod_gospit
    data_vypiski_old = patient.data_vypiski

    old_status = {
                'fio_zaveduyushchego_otd' : fio_zaveduyushchego_otd_old,
                'fio_lechashchego_vracha' : fio_lechashchego_vracha_old,
                'ppi'                       : ppi_old,
                'med_pokazaniya'            : med_pokazaniya_old,
                'dinamika_sostoyania'       : dinamika_sostoyania_old,
                'dvigatel_activnost'        : dvigatel_activnost_old,
                'status_nabludeniya'         : status_nabludeniya_old,
                'potrebnost_v_soc_koordinat' : potrebnost_v_soc_koordinat_old,

                'sposoben_virazit_soglasie' : sposoben_virazit_soglasie_old,
                'status_med_karty'          : status_med_karty_old,
                'status_po_mse'             : status_po_mse_old,
                'funkciional_kriterii' : funkciional_kriterii_old,

                'kommentarij' : kommentarij_old,
                'iskhod_gospit' : iskhod_gospit_old,
                'data_vypiski' : data_vypiski_old,
                }
    # ------------------- Шаги по сохранению изменений ---------- к

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------
        patient.fio_zaveduyushchego_otd = request.POST.get('fio_zaveduyushchego_otd')
        patient.fio_lechashchego_vracha = request.POST.get('fio_lechashchego_vracha')
        patient.ppi = request.POST.get('ppi')
        patient.med_pokazaniya = request.POST.get('med_pokazaniya')
        patient.dinamika_sostoyania = request.POST.get('dinamika_sostoyania')
        patient.dvigatel_activnost = request.POST.get('dvigatel_activnost')
        patient.status_nabludeniya = request.POST.get('status_nabludeniya')
        patient.potrebnost_v_soc_koordinat = request.POST.get('potrebnost_v_soc_koordinat')

        patient.sposoben_virazit_soglasie = request.POST.get('sposoben_virazit_soglasie')
        patient.status_med_karty = request.POST.get('status_med_karty')
        patient.status_po_mse = request.POST.get('status_po_mse')
        patient.funkciional_kriterii = request.POST.get('funkciional_kriterii')

        patient.kommentarij = request.POST.get('kommentarij')
        patient.iskhod_gospit = request.POST.get('iskhod_gospit')

        # ------------------- предотвращение ошибки из-за пустоты в ДАТЕ ----
        patient.data_vypiski = request.POST.get('data_vypiski')
        patient.data_vypiski = zamena_pustot(patient.data_vypiski)

        new_status = {
                    'fio_zaveduyushchego_otd': patient.fio_zaveduyushchego_otd,
                    'fio_lechashchego_vracha': patient.fio_lechashchego_vracha,
                    'ppi': patient.ppi,
                    'med_pokazaniya': patient.med_pokazaniya,
                    'dinamika_sostoyania': patient.dinamika_sostoyania,
                    'dvigatel_activnost': patient.dvigatel_activnost,
                    'status_nabludeniya': patient.status_nabludeniya,
                    'potrebnost_v_soc_koordinat': patient.potrebnost_v_soc_koordinat,
                    'sposoben_virazit_soglasie': patient.sposoben_virazit_soglasie,
                    'status_med_karty': patient.status_med_karty,
                    'status_po_mse': patient.status_po_mse,
                    'funkciional_kriterii': patient.funkciional_kriterii,
                    'kommentarij': patient.kommentarij,
                    'iskhod_gospit': patient.iskhod_gospit,
                    'data_vypiski': patient.data_vypiski,
                  }

    if 'btn_save_kriter' in request.POST:  # Кнопка "Сохранить"
        logger.info(
            f'пользователь {request.user} сохранил правки в Мед.блоке по -  {patient.fio_pacienta}')

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
                patient.data_last_changed_med = datetime.now()


        #  -------- проверка на ЕСТЬ необх СОЦ для записи даты передачи и приема в работу------------н
        if patient.potrebnost_v_soc_koordinat == '2. Есть потребность в соц.координаторе' and patient.data_peredachi_soc_koordinatoram_dtszn is None:
            patient.data_peredachi_soc_koordinatoram_dtszn = datetime.now()
            # patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = datetime.now()
        # elif patient.potrebnost_v_soc_koordinat == '2. Есть потребность в соц.координаторе' and patient.data_peredachi_soc_koordinatoram_dtszn is not None:
        #     patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = patient.data_peredachi_soc_koordinatoram_dtszn
        #  -------- проверка на ЕСТЬ необх СОЦ для записи даты передачи и приема в работу------------к

        patient.save()

        return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)

    elif 'btn_otmena_pravki_kriter' in request.POST:  # Кнопка "ОТМЕНИТЬ правки в критериях"
        logger.info(
            f'пользователь {request.user} отменил правки по kriter -  {patient.fio_pacienta}')
        return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'pravka_kriterij.html', {'patient': patient,
                                                    'status_last_date':status_last_date,
                                                    })



def v_kis_pravka_zayavka(request, id):
    patient = get_object_or_404(KisLong, id=id)
    # ---------- получаю из v_kis_pac_detail через сессию -------
    status_last_date = request.session.get('status_last_date')
    # ------------------- Шаги по сохранению изменений ---------- н
    soc_kriterii_old = patient.soc_kriterii
    tema_zayavki_pomosh_v_zhizneustrojstve_old = patient.tema_zayavki_pomosh_v_zhizneustrojstve
    nalichie_rodstvennikov_old = patient.nalichie_rodstvennikov
    status_pacienta_old = patient.status_pacienta
    soc_koordinator_old = patient.soc_koordinator
    status_resheniya_o_perevode_old = patient.status_resheniya_o_perevode
    poyasneniya_k_resheniyu_po_pac_old = patient.poyasneniya_k_resheniyu_po_pac
    reshenie_dtszn_po_putevke_old = patient.reshenie_dtszn_po_putevke

    data_resheniya_dtszn_old = patient.data_resheniya_dtszn
    data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn_old = patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn

    poluchatel_soc_uslug_old = patient.poluchatel_soc_uslug

    kommentarij_soc_koordinatorov_dtszn_old = patient.kommentarij_soc_koordinatorov_dtszn
    svedeniya_o_pac_peredani_dtszn_old = patient.svedeniya_o_pac_peredani_dtszn

    data_peredachi_sveden_v_dtszn_old = patient.data_peredachi_sveden_v_dtszn



    old_status = {
        'soc_kriterii': soc_kriterii_old,
        'tema_zayavki_pomosh_v_zhizneustrojstve': tema_zayavki_pomosh_v_zhizneustrojstve_old,
        'nalichie_rodstvennikov': nalichie_rodstvennikov_old,
        'status_pacienta': status_pacienta_old,
        'soc_koordinator': soc_koordinator_old,
        'status_resheniya_o_perevode': status_resheniya_o_perevode_old,
        'poyasneniya_k_resheniyu_po_pac': poyasneniya_k_resheniyu_po_pac_old,
        'reshenie_dtszn_po_putevke': reshenie_dtszn_po_putevke_old,
        'data_resheniya_dtszn': data_resheniya_dtszn_old,
        'kommentarij_soc_koordinatorov_dtszn': kommentarij_soc_koordinatorov_dtszn_old,
        'svedeniya_o_pac_peredani_dtszn': svedeniya_o_pac_peredani_dtszn_old,
        'data_peredachi_sveden_v_dtszn': data_peredachi_sveden_v_dtszn_old,
        'data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn': data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn_old,
        'poluchatel_soc_uslug': poluchatel_soc_uslug_old,
                  }
    # ------------------- Шаги по сохранению изменений ---------- к


    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # 2. Соц.критерии ---------------
        patient.soc_kriterii = request.POST.get('soc_kriterii')
        # 3. Состояние  заявки -------------склад автоматом
        # 4. Тема заявки_Помощь в жизнеустройстве ---
        patient.tema_zayavki_pomosh_v_zhizneustrojstve = request.POST.get('tema_zayavki_pomosh_v_zhizneustrojstve')
        # 5. Наличие     родственников---------------
        patient.nalichie_rodstvennikov = request.POST.get('nalichie_rodstvennikov')
        # 6. Дата передачи  соц.координаторам    ДТСЗН
        # 7. Дата принятия в работу соц координаторами  ДТСЗН
        # 8. Статус пациента (группа инвалидности)
        patient.status_pacienta = request.POST.get('status_pacienta')
        # 9. Соц.координатор (ФИО)
        patient.soc_koordinator = request.POST.get('soc_koordinator')
        # 10 .Статус решения о переводе
        patient.status_resheniya_o_perevode = request.POST.get('status_resheniya_o_perevode')
        # 11. Последняя дата изменения статуса решения о переводе
        # --- просто показываем последнюю дату ---
        # 12. Пояснения к решению о переводе
        patient.poyasneniya_k_resheniyu_po_pac = request.POST.get('poyasneniya_k_resheniyu_po_pac')
        patient.poluchatel_soc_uslug = request.POST.get('poluchatel_soc_uslug')
        # 13. Решение ДТСЗН по путевке
        patient.reshenie_dtszn_po_putevke = request.POST.get('reshenie_dtszn_po_putevke')
        # 14. Дата принятия решения ДТСЗН по путевке
        patient.data_resheniya_dtszn = request.POST.get('data_resheniya_dtszn')
        patient.data_resheniya_dtszn = zamena_pustot(patient.data_resheniya_dtszn)
        # print('wwwwwwwwwwwwwwwwwww')
        # print(zamena_pustot(patient.data_resheniya_dtszn), type(zamena_pustot(patient.data_resheniya_dtszn)))
        # print(data_resheniya_dtszn_old, '---', type(data_resheniya_dtszn_old))
        # print('wwwwwwwwwwwwwwwwwww')
        # 15. Комментарий соц координаторов ДТСЗН
        patient.kommentarij_soc_koordinatorov_dtszn = request.POST.get('kommentarij_soc_koordinatorov_dtszn')
        patient.svedeniya_o_pac_peredani_dtszn = request.POST.get('svedeniya_o_pac_peredani_dtszn')

        patient.data_peredachi_sveden_v_dtszn = request.POST.get('data_peredachi_sveden_v_dtszn')
        patient.data_peredachi_sveden_v_dtszn = zamena_pustot(patient.data_peredachi_sveden_v_dtszn)

        patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = request.POST.get('data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn')
        patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = zamena_pustot(patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn)




        new_status = {
            'soc_kriterii': patient.soc_kriterii,
            'tema_zayavki_pomosh_v_zhizneustrojstve': patient.tema_zayavki_pomosh_v_zhizneustrojstve,
            'nalichie_rodstvennikov': patient.nalichie_rodstvennikov,
            'status_pacienta': patient.status_pacienta,
            'soc_koordinator': patient.soc_koordinator,
            'status_resheniya_o_perevode': patient.status_resheniya_o_perevode,
            'poyasneniya_k_resheniyu_po_pac': patient.poyasneniya_k_resheniyu_po_pac,
            'reshenie_dtszn_po_putevke': patient.reshenie_dtszn_po_putevke,
            'data_resheniya_dtszn': patient.data_resheniya_dtszn,
            'kommentarij_soc_koordinatorov_dtszn': patient.kommentarij_soc_koordinatorov_dtszn,
            'svedeniya_o_pac_peredani_dtszn': patient.svedeniya_o_pac_peredani_dtszn,
            'data_peredachi_sveden_v_dtszn': patient.data_peredachi_sveden_v_dtszn,
            'data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn': patient.data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn,
            'poluchatel_soc_uslug': patient.poluchatel_soc_uslug,
        }


        if 'btn_save_pravki_zayavka' in request.POST:  # Кнопка "Сохранить"
            logger.info(
                f'пользователь {request.user} сохранил правки в Соц.блоке по -  {patient.fio_pacienta}')

            for key in old_status:
                # Сравниваем значения по ключам
                if old_status[key] != new_status[key]:
                    # Если значения отличаются, создаем новый объект KisChange
                    patient_changed = KisChange(  # Устанавливаем связь с объектом KisLong
                        id_pacienta=patient.id,  # Записываем название id пациента
                        fio_pacienta=patient.fio_pacienta,  # # Записываем название колонки
                        name_changed_colon=key,  # Записываем название колонки
                        data_old=old_status[key],  # Записываем старое значение
                        data_new=new_status[key],  # Записываем новое значение
                        time_changed=datetime.now(),  # Записываем новое значение
                        who_changed=request.user,  # Записываем новое значение
                    )
                    patient_changed.save()  # Сохраняем объект в базе данных
                    patient.data_last_changed_soc = datetime.now()
            patient.save()
            return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)

        elif 'btn_otmena_pravki_zayavka' in request.POST:  # Кнопка "ОТМЕНИТЬ правки в критериях"
            return redirect('app_kis_long:v_kis_pac_detail', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'pravka_zayavka.html', {'patient': patient,
                                                   'status_last_date':status_last_date,
                                                   })



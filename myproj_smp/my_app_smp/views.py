from django.shortcuts import render, get_object_or_404, redirect
from .models import SmpRazborTab
from django.db import connection
from django.core.paginator import Paginator
from django import forms
import datetime
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.http import HttpResponse
# from openpyxl import Workbook



# -----------------отслеж пользовательских входов ------------
from django.contrib.sessions.models import Session
from django.utils import timezone

# -----------------отслеж пользовательских входов ------------
def active_users_count(request):
    # Получаем текущее время
    now = timezone.now()
    # Устанавливаем время, после которого сессия считается неактивной (например, 5 минут)
    active_threshold = now - timezone.timedelta(minutes=0.5)

    # Получаем все активные сессии
    active_sessions = Session.objects.filter(expire_date__gte=now)

    # Подсчитываем количество уникальных пользователей
    active_user_ids = set()
    for session in active_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            active_user_ids.add(user_id)

    active_user_count = len(active_user_ids)
    # return active_user_count
    return render(request, 'login_statistics.html', {'active_user_count': active_user_count})

# -----------------отслеж пользовательских входов ------------


def calculate_date(chislo1, chislo2):
    #--------------- функция вычисления расчетных значений ДАТ:
    if chislo1 and chislo2:
        result = chislo1 - chislo2
    else:
        result = 'нет даты'
    return result


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            print(f"-----------------------------------------------------User {user} вошел")
            return redirect('my_app_smp:start_page')
            # return redirect('start_page')
        else:
            error_message = "Вас нет в списке"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)  # Выход из аккаунта
    print("-----------------------------------------00-----User logged out")  # Отладочное сообщение
    return redirect('login')  # Перенаправление на главную страницу


def start_page(request):

    return render(request, 'start.html')

def results(request):
    return render(request, 'results.html')

def zamena_pustot(pole_proverki_daty):
    # Функция проверки является ли значение в поле ДАТЫ - пустым??? для ВСЕХ ДАТ проверку!!!!
    # Проверяем ДАТУ, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
    if pole_proverki_daty == "":
        pole_proverki_daty = None
    else:
        pole_proverki_daty = pole_proverki_daty
    return pole_proverki_daty

def help(request):
    return render(request, 'help.html', {
    })

# @login_required
def home(request):

    # dict_vps = {'butovo':	'Бутово',
    #             'voronovo':	'Вороново',
    #             'danilovskij'	:'Даниловский',
    #             'degunino'	:'Дегунино',
    #             'zelenograd'	:'Зеленоград ОВПП',
    #             'kolomenskoe':	'Коломенское ОВПП',
    #             'kurkino':	'Куркино ОВПП',
    #             'lyublino'	: 'Люблино ОВПП',
    #             'nekrasovka':	'Некрасовка ОВПП',
    #             'ovprp'	:'ОВПРП',
    #             'pmdkh':	'ПМДХ ОВПП',
    #             'pmkh'	:'ПМХ ОВПП',
    #             'preobrazhenskoe':	'Преображенское ОВПП',
    #             'rostokino':'Ростокино ОВПП',
    #             'savelovskij'	:'Савеловский ОВПП',
    #             'solncevo'	: 'Солнцево',
    #             'khoroshevo':	'Хорошево ОВПП',
    #             'caricyno':	'Царицыно ОВПП',}

    # --------------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # groups = Group.objects.all()
    print(user_groups_list)
    print(request.user)

    # --------------

    # ----------------------- отбор списка ВПС
    unique_kurir = SmpRazborTab.objects.values_list('kuriruyushchee_podrazdelenie_ovpp', flat=True).distinct()
    unique_kurir_list = []
    for i in unique_kurir:
        print(i)
        unique_kurir_list.append(str(i))
    print()
    # -----------------------

    is_vps_group = request.user.groups.filter(name='vps').exists()
    query_fio = request.GET.get('search_fio', '')  # Получаем строку поиска по FIO
    query_kurir = request.GET.get('search_kurir', '')  # Получаем строку поиска по курирующему подразделению
    query_otrabot = request.GET.get('search_otrabot', '')  # Получаем строку поиска по отработанным записям
    records_per_page = request.GET.get('records_per_page', 20)  # Получаем количество записей на странице

    # query_kurir = dict_vps.get(str(request.user))
    # print(query_kurir)
    # ---------------- отсеим на входе по ЮЗЕРУ - к какой ВПС он принадлежит ------------

    print('-----------')
    print(unique_kurir)
    # user_vps_substring = dict_vps.get(str(request.user))
    # print(user_vps_substring)
    # query_kurir = list(filter(lambda item: user_vps_substring in item, unique_kurir))

    print(query_kurir)  # Вывод: ['banana', 'grape']

    # Обработка фильтров из GET-запроса
    if request.method == 'GET':
        if 'search_fio' in request.GET:
            query_fio = request.GET.get('search_fio', '')

        if 'search_kurir' in request.GET:
            query_kurir = request.GET.get('search_kurir', '')

        if 'search_otrabot' in request.GET:
            query_otrabot = request.GET.get('search_otrabot', '')

    # Фильтруем данные по обоим полям и сортируем по p_p
    # data_smp = SmpRazborTab.objects.all().order_by('p_p')  # Сортировка по возрастанию p_p
    # Фильтруем данные по обоим полям
    if user_groups_list == ['vps']:
        # Исключаем записи, у которых ok_vps равно "ВПС"
        data_smp = SmpRazborTab.objects.filter(ok_vps="впс").order_by('data_vyzova_smp',
                                                                                  'fio_pacienta')  # Сортировка по возрастанию
    else:
        data_smp = SmpRazborTab.objects.all().order_by('data_vyzova_smp', 'fio_pacienta')  # Сортировка по возрастанию
    total_records = data_smp.count()  # Общее количество записей

    if query_fio:
        data_smp = data_smp.filter(fio_pacienta__icontains=query_fio)

    if query_kurir:
        data_smp = data_smp.filter(kuriruyushchee_podrazdelenie_ovpp__icontains=query_kurir)

    if query_otrabot:
        data_smp = data_smp.filter(ok_vps=query_otrabot)

    # Получаем уникальные значения для выпадающего списка
    unique_kurir = SmpRazborTab.objects.values_list('kuriruyushchee_podrazdelenie_ovpp', flat=True).distinct()
    unique_otrab = SmpRazborTab.objects.values_list('ok_vps', flat=True).distinct()

    paginator = Paginator(data_smp, records_per_page)  # Показывать 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'data_smp': page_obj,
        'search_fio': query_fio,
        'search_kurir': query_kurir,
        'search_otrabot': query_otrabot,
        'records_per_page': records_per_page,
        'total_records': total_records,  # Передаем общее количество записей
        'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст по курир. филиалу ВПС
        'unique_otrab': unique_otrab,  # Передаем уникальные значения в контекст по отработанным в КЭР
        'groups': user_groups_list, # Получаем все группы
    })



def patient_detail(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)  # Получаем запись по ID

    return render(request, 'patient_detail.html', {'patient': patient})


def edit_patient(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)

    # --------------- вычсление перес=менных по ДНЯМ!!! ------------
    koli4_dney_ot_proshlogo_vizita_vracha = calculate_date(patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu,
                                                           patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias)
    dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = calculate_date(patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc,
                                                           patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------
        patient.fio_vracha = request.POST.get('fio_vracha')
        patient.sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle = request.POST.get(
            'sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle')
        patient.dejstviya_cpp = request.POST.get('dejstviya_cpp')
        patient.kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij = request.POST.get(
            'kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij')
        patient.vyvod = request.POST.get('vyvod')

        # -----------------------------Данные из последнего протокола врача --------------------------

        patient.byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite = request.POST.get(
            'byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite')
        patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = request.POST.get(
            'kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu')

        # Проверяем, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = zamena_pustot(patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu)

        # -----------------
        patient.otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme = request.POST.get(
            'otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme')
        patient.dinamika_sostoyaniya = request.POST.get('dinamika_sostoyaniya')

        # -----Начало блока проверки даты------ получение ДАТЫ и ее проверка на пустоту!!!--------
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = request.POST.get(
            'data_naznachenogo_audioprotokola_soglasno_protokolu_v')
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = zamena_pustot(
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)
        # ---------Конец блока проверки даты- получение ДАТЫ и ее проверка на пустоту!!!-----------


        # -----------------------------Проверка заведующего --------------------------
        # -----Начало блока проверки даты------ получение ДАТЫ и ее проверка на пустоту!!!--------
        patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc = request.POST.get(
            'data_polucheniya_svedenij_po_vyzovam_smp_ot_kc')
        patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc = zamena_pustot(
            patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc)
        # ---------Конец блока проверки даты- получение ДАТЫ и ее проверка на пустоту!!!-----------

        # -----Начало блока проверки даты------ получение ДАТЫ и ее проверка на пустоту!!!--------
        patient.data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp = request.POST.get(
            'data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp')
        patient.data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp = zamena_pustot(
            patient.data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp)
        # ---------Конец блока проверки даты- получение ДАТЫ и ее проверка на пустоту!!!-----------


        patient.kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya = request.POST.get(
            'kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya')
        patient.kakie_dejstviya_byli_predprinyaty_smp = request.POST.get('kakie_dejstviya_byli_predprinyaty_smp')
        patient.tekushchee_sostoyanie_pacienta_posle_vyzova_smp = request.POST.get(
            'tekushchee_sostoyanie_pacienta_posle_vyzova_smp')
        patient.ostalis_li_zhaloby_posle_vyzova_smp = request.POST.get('ostalis_li_zhaloby_posle_vyzova_smp')
        patient.opisanie_zhalob = request.POST.get('opisanie_zhalob')
        patient.byli_li_lekarstvennye_sredstva_otovareny_po_receptu = request.POST.get(
            'byli_li_lekarstvennye_sredstva_otovareny_po_receptu')
        patient.pacient_prinimaet_naznachennye_lekarstvennye_sredstva = request.POST.get(
            'pacient_prinimaet_naznachennye_lekarstvennye_sredstva')
        patient.ehffektivna_li_naznachennaya_medikamentoznaya_terapiya = request.POST.get(
            'ehffektivna_li_naznachennaya_medikamentoznaya_terapiya')
        patient.est_li_pobochnye_dejstviya_ot_naznachennykh_lekarstvennykh = request.POST.get(
            'est_li_pobochnye_dejstviya_ot_naznachennykh_lekarstvennykh')
        patient.pacientu_byla_ozvuchena_data_sleduyushchego_vizita = request.POST.get(
            'pacientu_byla_ozvuchena_data_sleduyushchego_vizita')
        patient.pacientu_byli_predostavleny_kontaktnye_nomera_cpp = request.POST.get(
            'pacientu_byli_predostavleny_kontaktnye_nomera_cpp')
        patient.pacient_zvonil_po_ukazannym_kontaktnym_nomera_do_vyzova_smp = request.POST.get(
            'pacient_zvonil_po_ukazannym_kontaktnym_nomera_do_vyzova_smp')
        patient.prichina_po_kotoroj_pacient_ne_zvonil_po_ukazannym_nomeram = request.POST.get(
            'prichina_po_kotoroj_pacient_ne_zvonil_po_ukazannym_nomeram')
        patient.sootvetstvuet_li_naznachennyj_bazovyj_plan_sostoyaniyu_pacie = request.POST.get(
            'sootvetstvuet_li_naznachennyj_bazovyj_plan_sostoyaniyu_pacie')
        patient.trebovanie_gospitalizacii_na_dannyj_moment = request.POST.get(
            'trebovanie_gospitalizacii_na_dannyj_moment')
        patient.vyyavlennye_defekty_v_rabote_vracha = request.POST.get('vyyavlennye_defekty_v_rabote_vracha')

        # -----------------------
        print('1ssssss-----------------')
        if 'save' in request.POST:  # Кнопка "Сохранить"
            # ------------------- сохраняю расчетные значения по КОЛИЧЕСТВУ дней в БД -------------
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover

            patient.save()
            return redirect('my_app_smp:home')

        elif 'send_to_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            # ------------------- сохраняю расчетные значения по КОЛИЧЕСТВУ дней в БД -------------
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover
            print('kolichestvo_dnej_ot_proshlogo_vizita_vracha-----------------', koli4_dney_ot_proshlogo_vizita_vracha)
            print('kolichestvo_dnej_ot_proshlogo_vizita_vracha-----------------', dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover)
            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:proverka', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'edit_pacient_short.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover': dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })


def edit_ker(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    #  ----- отображение рассчетных ДННЕЙ+++++++--------------------
    koli4_dney_ot_proshlogo_vizita_vracha = calculate_date(patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu,
                                                           patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias)
    dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = calculate_date(patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc,
                                                           patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать и СОХРАНЯТЬ!!!

        # --------------- поля для редактирования и сохранения --------
        patient.bazovyj_plan_naznachen_korrektno = request.POST.get('bazovyj_plan_naznachen_korrektno')
        patient.ocenka_sostoyaniya_sootvetstvuet_bazovomu_planu = request.POST.get('ocenka_sostoyaniya_sootvetstvuet_bazovomu_planu')
        patient.zhaloby_opisany_v_polnom_obeme = request.POST.get('zhaloby_opisany_v_polnom_obeme')
        patient.ocenka_zaveduyushchego_proizvedena_korrektno = request.POST.get('ocenka_zaveduyushchego_proizvedena_korrektno')
        patient.ocenka_dejstvij_vracha_do_vyzova_smp = request.POST.get('ocenka_dejstvij_vracha_do_vyzova_smp')
        patient.ocenka_dejstvij_posle_vyzova_smp = request.POST.get('ocenka_dejstvij_posle_vyzova_smp')
        patient.vyvody_po_rezultatm_ocenki = request.POST.get('vyvody_po_rezultatm_ocenki')

        # patient.save()  # Сохраняем изменения

        print('1ker-----------------')
        if 'save_ker' in request.POST:  # Кнопка "Сохранить"
            # if patient.is_valid():
            # ------------------- сохраняю расчетные значения по КОЛИЧЕСТВУ дней в БД -------------
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover

            patient.save()
            return redirect('my_app_smp:home')

        elif 'return_na_vps' in request.POST:  # Кнопка "Отправить в ВПС"
            patient.ok_vps = "впс"
            # ------------------- сохраняю расчетные значения по КОЛИЧЕСТВУ дней в БД -------------
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover


            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:home')  # Переходим на страницу проверки

        elif 'go_gv' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано Глав.врачу"
            # ------------------- сохраняю расчетные значения по КОЛИЧЕСТВУ дней в БД -------------
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover

            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:proverka_ker', id=patient.id)  # Переходим на страницу проверки

        return redirect('my_app_smp:home',

                        )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_ker.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover':dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })


def proverka(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    # --------------- вычсление перес=менных по ДНЯМ!!! ------------
    koli4_dney_ot_proshlogo_vizita_vracha = calculate_date(patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu,
                                                           patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias)
    dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = calculate_date(patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc,
                                                           patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)

    if request.method == 'POST':
        if 'ot_vps_v_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано в КЭР"
            patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha = koli4_dney_ot_proshlogo_vizita_vracha
            patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover

            patient.save()
            return redirect('my_app_smp:home')  # Переходим на главную страницу

        elif 'korrektirovat' in request.POST:  # Кнопка "Корректировать"
            return redirect('my_app_smp:edit_patient', id=id)  # Возвращаем на страницу редактирования

    return render(request, 'patient_detail.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover':dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })



def proverka_ker(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    if request.method == 'POST':
        if 'ot_ker_na_glav' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано Глав.врачу"
            patient.save()
            return redirect('my_app_smp:home')  # Переходим на главную страницу

        elif 'korrektirovat_ker' in request.POST:  # Кнопка "Корректировать"
            patient.ok_vps = "Передано в КЭР"
            patient.save()
            return redirect('my_app_smp:home')  # Возвращаем на страницу редактирования

    return render(request, 'proverka_ot_ker_na_glav.html', {'patient': patient})

def edit_glav(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    #  ----- отображение рассчетных ДННЕЙ+++++++--------------------
    koli4_dney_ot_proshlogo_vizita_vracha = calculate_date(patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu,
                                                           patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias)
    dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = calculate_date(patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc,
                                                           patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать и СОХРАНЯТЬ!!!
        # 'analiz_dejstvij_glavnym_vrachom',

        # --------------- поля для редактирования и сохранения --------
        patient.analiz_dejstvij_glavnym_vrachom = request.POST.get('analiz_dejstvij_glavnym_vrachom')


        # patient.save()  # Сохраняем изменения

        print('1ker-----------------')
        if 'save_glav' in request.POST:  # Кнопка "Сохранить"
            # if patient.is_valid():
            patient.save()
            return redirect('my_app_smp:home')

        elif 'return_na_vps' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "впс"
            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:home')  # Переходим на страницу проверки

        elif 'return_na_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано КЭР"
            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:home')  # Переходим на страницу проверки

        elif 'go_dzm' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано ДЗМ"
            patient.save()  # Сохраняем изменения
            return redirect('my_app_smp:proverka_glav', id=patient.id)  # Переходим на страницу проверки

        return redirect('my_app_smp:home',

                        )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_glav.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover':dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })

def proverka_glav(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    if request.method == 'POST':
        if 'ot_glav_na_dzm' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано ДЗМ"
            patient.save()
            return redirect('my_app_smp:home')  # Переходим на главную страницу

        elif 'korrektir_glav' in request.POST:  # Кнопка "Корректировать"
            patient.ok_vps = "Передано Глав.врачу"
            patient.save()
            return redirect('my_app_smp:home')  # Возвращаем на страницу редактирования

    return render(request, 'proverka_ot_glav.html', {'patient': patient})



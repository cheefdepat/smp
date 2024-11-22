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




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('my_app_smp:start_page')
            # return redirect('start_page')
        else:
            error_message = "Вас нет в списке"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)  # Выход из аккаунта
    print("User logged out")  # Отладочное сообщение
    return redirect('login')  # Перенаправление на главную страницу
    # return render(request, 'login.html')

def start_page(request):
    return render(request, 'start.html')


# class MyprojectLogout(LogoutView):
#     next_page  = reverse_lazy('login')

def zamena_pustot(pole_proverki_daty):
    # Функция проверки является ли значение в поле ДАТЫ - пустым??? для ВСЕХ ДАТ проверку!!!!
    if pole_proverki_daty == "":
        pole_proverki_daty = None
    else:
        pole_proverki_daty = pole_proverki_daty
    return pole_proverki_daty

def help(request):
    return render(request, 'help.html', {
        # 'data_smp': page_obj,
        # 'search_fio': query_fio,
        # 'search_kurir': query_kurir,
        # 'search_otrabot': query_otrabot,
        # 'records_per_page': records_per_page,
        # 'total_records': total_records,  # Передаем общее количество записей
        # 'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст по курир. филиалу ВПС
        # 'unique_otrab': unique_otrab,  # Передаем уникальные значения в контекст по отработанным в КЭР
        # 'groups': user_groups_list,  # Получаем все группы
    })

# @login_required
def home(request):
    # --------------
    # user_groups = request.user.groups.all()
    # print(user_groups)
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # groups = Group.objects.all()
    print(user_groups_list)
    #
    # print(groups[1])
    # print(groups)
    # print('ker' not in groups)
    # --------------

    is_vps_group = request.user.groups.filter(name='vps').exists()
    query_fio = request.GET.get('search_fio', '')  # Получаем строку поиска по FIO
    query_kurir = request.GET.get('search_kurir', '')  # Получаем строку поиска по курирующему подразделению
    query_otrabot = request.GET.get('search_otrabot', '')  # Получаем строку поиска по отработанным записям
    records_per_page = request.GET.get('records_per_page', 10)  # Получаем количество записей на странице

    # Фильтруем данные по обоим полям и сортируем по p_p
    # data_smp = SmpRazborTab.objects.all().order_by('p_p')  # Сортировка по возрастанию p_p
    # Фильтруем данные по обоим полям
    print(request.user.groups)

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



    # data_smp = data_smp.filter(ok_vps=query_kurir)
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



# @login_required
def patient_detail(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)  # Получаем запись по ID

    return render(request, 'patient_detail.html', {'patient': patient})


def edit_patient(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)

    # --------------- вычсление перес=менных по ДНЯМ!!! ------------

    if patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu and patient.data_vklyucheniya_v_registr:
        koli4_dney_ot_proshlogo_vizita_vracha = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu - patient.data_vklyucheniya_v_registr
    else:
        koli4_dney_ot_proshlogo_vizita_vracha = 'нет даты визита врача'

    if patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc and patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc - patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
    else:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = 'нет звонка или  врача'


    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------

        # 'fio_vracha',
        # 'sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle',
        # 'dejstviya_cpp',
        # 'kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij',
        # 'vyvod',

        patient.fio_vracha = request.POST.get('fio_vracha')
        patient.sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle = request.POST.get(
            'sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle')
        patient.dejstviya_cpp = request.POST.get('dejstviya_cpp')
        patient.kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij = request.POST.get(
            'kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij')
        patient.vyvod = request.POST.get('vyvod')

        # -----------------------------Данные из последнего протокола врача --------------------------
        # 'byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite',
        # 'kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu',
        # 'kolichestvo_dnej_ot_proshlogo_vizita_vracha',
        # 'otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme',
        # 'dinamika_sostoyaniya',
        # 'data_naznachenogo_audioprotokola_soglasno_protokolu_v',

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
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = request.POST.get(
            'data_naznachenogo_audioprotokola_soglasno_protokolu_v')

        # Проверяем ДАТУ, является ли значение None ---------------- для ВСЕХ ДАТ проверку!!!!
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = zamena_pustot(
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v)

        # -----------------------------Проверка заведующего --------------------------

        # 'data_polucheniya_svedenij_po_vyzovam_smp_ot_kc',
        # 'data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp',
        # 'kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover',
        #
        # 'kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya',
        # 'kakie_dejstviya_byli_predprinyaty_smp',
        # 'tekushchee_sostoyanie_pacienta_posle_vyzova_smp',
        # 'ostalis_li_zhaloby_posle_vyzova_smp',
        # 'opisanie_zhalob',
        # 'byli_li_lekarstvennye_sredstva_otovareny_po_receptu',
        # 'pacient_prinimaet_naznachennye_lekarstvennye_sredstva',
        # 'ehffektivna_li_naznachennaya_medikamentoznaya_terapiya',
        # 'est_li_pobochnye_dejstviya_ot_naznachennykh_lekarstvennykh',
        # 'pacientu_byla_ozvuchena_data_sleduyushchego_vizita',
        # 'pacientu_byli_predostavleny_kontaktnye_nomera_cpp',
        # 'pacient_zvonil_po_ukazannym_kontaktnym_nomera_do_vyzova_smp',
        # 'prichina_po_kotoroj_pacient_ne_zvonil_po_ukazannym_nomeram',
        # 'sootvetstvuet_li_naznachennyj_bazovyj_plan_sostoyaniyu_pacie',
        # 'trebovanie_gospitalizacii_na_dannyj_moment',
        # 'vyyavlennye_defekty_v_rabote_vracha',


        # --------------------Проверяем ДАТУ !!!!--------------------------------------------------
        patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc = zamena_pustot(
                                                                patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc)


        # --------------------Проверяем ДАТУ !!!!--------------------------------------------------
        patient.data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp = zamena_pustot(
            patient.data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp)


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
        # patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = request.POST.get(
        #     'kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover')
        # -----------------------
        print('1ssssss-----------------')
        if 'save' in request.POST:  # Кнопка "Сохранить"
            print('ssssss-----------------')
            # if patient.is_valid():
            patient.save()
            return redirect('home')

        elif 'send_to_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            # if patient.is_valid():
            print('send_to_ker-----------------')
            patient.save()  # Сохраняем изменения
            return redirect('proverka', id=patient.id)  # Переходим на страницу проверки

        # patient.save()  # Сохраняем изменения
        # return redirect('home',
        #
        #                 )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_short.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover': dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })

def edit_ker(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    #  ----- отображение рассчетных ДННЕЙ+++++++--------------------

    if patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu and patient.data_vklyucheniya_v_registr:
        koli4_dney_ot_proshlogo_vizita_vracha = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu - patient.data_vklyucheniya_v_registr
    else:
        koli4_dney_ot_proshlogo_vizita_vracha = 'нет даты визита врача'

    if patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc and patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc - patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
    else:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = 'нет звонка или  врача'



    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать и СОХРАНЯТЬ!!!
        # 'bazovyj_plan_naznachen_korrektno',
        # 'ocenka_sostoyaniya_sootvetstvuet_bazovomu_planu',
        # 'zhaloby_opisany_v_polnom_obeme',
        # 'ocenka_zaveduyushchego_proizvedena_korrektno',
        # 'ocenka_dejstvij_vracha_do_vyzova_smp',
        # 'ocenka_dejstvij_posle_vyzova_smp',
        # 'vyvody_po_rezultatm_ocenki',
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
            patient.save()
            return redirect('home')

        elif 'return_na_vps' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "впс"
            patient.save()  # Сохраняем изменения
            return redirect('home')  # Переходим на страницу проверки

        elif 'go_gv' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано Глав.врачу"
            patient.save()  # Сохраняем изменения
            return redirect('proverka_ker', id=patient.id)  # Переходим на страницу проверки

        return redirect('home',

                        )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_ker.html', {'patient': patient,
                                                       'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover':dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })


def proverka(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)

    if request.method == 'POST':
        if 'ot_vps_v_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано в КЭР"
            patient.save()
            return redirect('home')  # Переходим на главную страницу

        elif 'korrektirovat' in request.POST:  # Кнопка "Корректировать"
            return redirect('edit_patient', id=id)  # Возвращаем на страницу редактирования

    return render(request, 'patient_detail.html', {'patient': patient})



def proverka_ker(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    if request.method == 'POST':
        if 'ot_ker_na_glav' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано Глав.врачу"
            patient.save()
            return redirect('home')  # Переходим на главную страницу

        elif 'korrektirovat_ker' in request.POST:  # Кнопка "Корректировать"
            patient.ok_vps = "Передано в КЭР"
            patient.save()
            return redirect('home')  # Возвращаем на страницу редактирования

    return render(request, 'proverka_ot_ker_na_glav.html', {'patient': patient})

def edit_glav(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)
    #  ----- отображение рассчетных ДННЕЙ+++++++--------------------

    if patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu and patient.data_vklyucheniya_v_registr:
        koli4_dney_ot_proshlogo_vizita_vracha = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu - patient.data_vklyucheniya_v_registr
    else:
        koli4_dney_ot_proshlogo_vizita_vracha = 'нет даты визита врача'

    if patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc and patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc - patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
    else:
        dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = 'нет звонка или  врача'



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
            return redirect('home')

        elif 'return_na_vps' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "впс"
            patient.save()  # Сохраняем изменения
            return redirect('home')  # Переходим на страницу проверки

        elif 'return_na_ker' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано КЭР"
            patient.save()  # Сохраняем изменения
            return redirect('home')  # Переходим на страницу проверки

        elif 'go_dzm' in request.POST:  # Кнопка "Отправить в КЭР"
            patient.ok_vps = "Передано ДЗМ"
            patient.save()  # Сохраняем изменения
            return redirect('proverka_glav', id=patient.id)  # Переходим на страницу проверки

        return redirect('home',

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
            return redirect('home')  # Переходим на главную страницу

        elif 'korrektir_glav' in request.POST:  # Кнопка "Корректировать"
            patient.ok_vps = "Передано Глав.врачу"
            patient.save()
            return redirect('home')  # Возвращаем на страницу редактирования

    return render(request, 'proverka_ot_glav.html', {'patient': patient})
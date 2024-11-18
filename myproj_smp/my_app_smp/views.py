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
            return redirect('home')
        else:
            error_message = "Вас нет в списке"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)  # Выход из аккаунта
    print("User logged out")  # Отладочное сообщение
    return redirect('login')  # Перенаправление на главную страницу
    # return render(request, 'login.html')


# class MyprojectLogout(LogoutView):
#     next_page  = reverse_lazy('login')


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
    # if request.user.is_authenticated and request.user.groups.filter(name='vps').exists():
    if user_groups_list == ['vps']:
        # Исключаем записи, у которых ok_vps равно "Передано в КЭР"
        data_smp = SmpRazborTab.objects.exclude(ok_vps="Передано в КЭР").order_by('data_vyzova_smp',
                                                                                  'fio_pacienta')  # Сортировка по возрастанию
    else:
        data_smp = SmpRazborTab.objects.all().order_by('data_vyzova_smp', 'fio_pacienta')  # Сортировка по возрастанию
    total_records = data_smp.count()  # Общее количество записей

    if query_fio:
        data_smp = data_smp.filter(fio_pacienta__icontains=query_fio)

    if query_kurir:
        data_smp = data_smp.filter(kuriruyushchee_podrazdelenie_ovpp__icontains=query_kurir)


    # data_smp = data_smp.filter(ok_vps=query_kurir)
    # Получаем уникальные значения для выпадающего списка
    unique_kurir = SmpRazborTab.objects.values_list('kuriruyushchee_podrazdelenie_ovpp', flat=True).distinct()

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
        'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст
        'groups': user_groups_list, # Получаем все группы
    })

# @login_required
def patient_detail(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)  # Получаем запись по ID

    return render(request, 'patient_detail.html', {'patient': patient})

# @login_required
def edit_patient(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)

    if patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias:
        dni =  datetime.date.today() - patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias
    else: dni = 'нет даты визита врача'

    if patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc and patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v:
        dni_zvon =  patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc - patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
    else: dni_zvon = 'нет звонка или  врача'


    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # patient.polis_oms = request.POST.get('polis_oms')
        # patient.kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya = request.POST.get('kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya')
        # patient.vyvody_po_rezultatm_ocenki = request.POST.get('vyvody_po_rezultatm_ocenki')
        # patient.zhaloby_opisany_v_polnom_obeme = request.POST.get('zhaloby_opisany_v_polnom_obeme')


        # --------------- поля для редактирования и сохранения --------
        patient.byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite = request.POST.get('byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite')
        patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = request.POST.get('kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu')
        # -----------------
        # Получаем значение из формы
        # next_visit_date = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu
        # Проверяем, является ли значение None
        if patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu == "":
            patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = None
        else:
            patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu
        # -----------------


        patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha= request.POST.get('kolichestvo_dnej_ot_proshlogo_vizita_vracha')
        patient.otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme= request.POST.get('otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme')
        patient.dinamika_sostoyaniya= request.POST.get('dinamika_sostoyaniya')
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v= request.POST.get('data_naznachenogo_audioprotokola_soglasno_protokolu_v')
        # Проверяем, является ли значение None
        if patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v == "":
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = None
        else:
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
        # -----------------
        patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = request.POST.get(
            'kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover')

        patient.save()  # Сохраняем изменения
        return redirect('home',

                        )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_short.html', {'patient': patient,
                                                       'dni': dni,
                                                       'dni_zvon':dni_zvon,
                                                       })

def edit_ker(request, id):
    patient = get_object_or_404(SmpRazborTab, id=id)

    if patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias:
        dni =  datetime.date.today() - patient.data_poslednego_vizita_vracha_iz_protokola_osmotra_emias
    else: dni = 'нет даты визита врача'

    if patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc and patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v:
        dni_zvon =  patient.data_polucheniya_svedenij_po_vyzovam_smp_ot_kc - patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
    else: dni_zvon = 'нет звонка или врача'


    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # patient.polis_oms = request.POST.get('polis_oms')
        # patient.kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya = request.POST.get('kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya')
        # patient.vyvody_po_rezultatm_ocenki = request.POST.get('vyvody_po_rezultatm_ocenki')
        # patient.zhaloby_opisany_v_polnom_obeme = request.POST.get('zhaloby_opisany_v_polnom_obeme')


        # --------------- поля для редактирования и сохранения --------
        patient.byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite = request.POST.get('byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite')
        patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = request.POST.get('kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu')
        # -----------------
        # Получаем значение из формы
        # next_visit_date = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu
        # Проверяем, является ли значение None
        if patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu == "":
            patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = None
        else:
            patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = patient.kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu
        # -----------------


        patient.kolichestvo_dnej_ot_proshlogo_vizita_vracha= request.POST.get('kolichestvo_dnej_ot_proshlogo_vizita_vracha')
        patient.otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme= request.POST.get('otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme')
        patient.dinamika_sostoyaniya= request.POST.get('dinamika_sostoyaniya')
        patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v= request.POST.get('data_naznachenogo_audioprotokola_soglasno_protokolu_v')
        # Проверяем, является ли значение None
        if patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v == "":
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = None
        else:
            patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v = patient.data_naznachenogo_audioprotokola_soglasno_protokolu_v
        # -----------------
        patient.kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = request.POST.get(
            'kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover')

        patient.save()  # Сохраняем изменения
        return redirect('home',

                        )  # Перенаправляем на главную страницу

    return render(request, 'edit_pacient_ker.html', {'patient': patient,
                                                       'dni': dni,
                                                       'dni_zvon':dni_zvon,
                                                       })


def send_to_ker(request, id):
    record = get_object_or_404(SmpRazborTab, id=id)
    record.ok_vps = "Передано в КЭР"  # Изменяем состояние поля
    record.save()  # Сохраняем изменения

    return redirect('home')  # Перенаправляем на нужный URL
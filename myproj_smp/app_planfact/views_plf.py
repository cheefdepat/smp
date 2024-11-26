from django.shortcuts import render, get_object_or_404, redirect
from .models import PlanFactTab
# import datetime
from django.core.paginator import Paginator



def plf_start_list(request):
    dict_vps_plf = {'butovo': 'Бутово',
                'voronovo': 'Вороново ОВПП',
                'danilovskij': 'Даниловский ОВПП',
                'degunino': 'Филиал "Дегунино" ММЦПП ДЗМ',
                'zelenograd': 'Филиал "Зеленоград" ММЦПП ДЗМ',
                'kolomenskoe': 'Филиал "Коломенское" ММЦПП ДЗМ',
                'kurkino': 'Куркино ОВПП',
                'lyublino': 'Люблино ОВПП',
                'nekrasovka': 'Некрасовка ОВПП',
                'ovprp': 'ОВПРП',
                'pmdkh': 'ПМДХ ОВПП',
                'pmkh': 'ПМХ ОВПП',
                'preobrazhenskoe': 'Преображенское ОВПП',
                'rostokino': 'Ростокино ОВПП',
                'savelovskij': 'Савеловский ОВПП',
                'solncevo': 'Солнцево ОВПП',
                'khoroshevo': 'Хорошево ОВПП',
                'caricyno': 'Царицыно ОВПП', }

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

    return render(request, 'planfact_home_page.html', {
        'data_plf': page_obj,
        'search_fio': query_fio,
        'search_kurir': query_kurir,
        'search_otrabot': query_otrabot,
        'records_per_page': records_per_page,
        'total_records': total_records,  # Передаем общее количество записей
        'unique_kurir': unique_kurir,  # Передаем уникальные значения в контекст по курир. филиалу ВПС
        'unique_otrab': unique_otrab,  # Передаем уникальные значения в контекст по отработанным в КЭР
         'search_data_zamecaniya': query_data_zamecaniya,  # Передаем уникальные значения в контекст по отработанным в КЭР

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
from django.shortcuts import render
import logging
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import IdReesrtFio
from django.db.models import Q
from django.core.paginator import Paginator



def zamena_pustot(pole_proverki_daty):
    # Функция проверки является ли значение в поле ДАТЫ - пустым??? для ВСЕХ ДАТ проверку!!!!
    if pole_proverki_daty == "":
        pole_proverki_daty = None
    else:
        pole_proverki_daty = pole_proverki_daty
    return pole_proverki_daty

def v_id_add_svedeniya_o_pac(request):
    patients = IdReesrtFio.objects.filter(Q(fio_pacienta__isnull=True) | Q(fio_pacienta='') | Q(fio_pacienta='None'))

    # --------------
    user_groups_list = []
    for i in request.user.groups.all():
        print(i)
        user_groups_list.append(str(i))
    # --------------

    query_fio = request.GET.get('search_fio', '')  # Получаем строку поиска по FIO
    query_id = request.GET.get('search_id', '')  # Получаем строку поиска по FIO
    query_oms = request.GET.get('search_oms', '')  # Получаем строку поиска по FIO

    records_per_page = request.GET.get('records_per_page', 20)  # Получаем количество записей на странице


    # Получаем уникальные значения для выпадающего списка
    patients = IdReesrtFio.objects.all()
    patients_filtr = IdReesrtFio.objects.all()
    # patients = IdReesrtFio.objects.filter(Q(fio_pacienta__isnull=True) | Q(fio_pacienta='')| Q(fio_pacienta='None'))
    search_fio_status = request.GET.get('search_fio_status', '')

    if search_fio_status == 'filled':
        patients_filtr = patients_filtr.exclude(Q(fio_pacienta__isnull=True) | Q(fio_pacienta=''))
    elif search_fio_status == 'empty':
        patients_filtr = patients_filtr.filter(
            Q(fio_pacienta__isnull=True) | Q(fio_pacienta='') | Q(fio_pacienta='None') | Q(fio_pacienta='нет'))


    # Обработка фильтров из GET-запроса
    if request.method == 'GET':
        if 'records_per_page' in request.GET and request.GET['records_per_page'] != '':
            request.session['records_per_page'] = int(request.GET['records_per_page'])
        records_per_page = request.GET.get('records_per_page', request.session.get('records_per_page', 20))

        if 'search_fio' in request.GET:
            query_fio = request.GET.get('search_fio', '')

        if 'search_id' in request.GET:
            query_id = request.GET.get('search_id', '')

        if 'search_oms' in request.GET:
            query_oms = request.GET.get('search_oms', '')


    # Фильтруем данные

    total_records = patients.count()  # Общее количество записей

    if query_fio:
        patients_filtr = patients_filtr.filter(fio_pacienta__icontains=query_fio)

    if query_id:
        patients_filtr = patients_filtr.filter(id_pac__icontains=query_id)
    if query_oms:
        patients_filtr = patients_filtr.filter(polis_oms__icontains=query_oms)




    paginator = Paginator(patients_filtr, records_per_page)  # Показывать 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter_records = patients_filtr.count()  #  количество записей - отфильтрованное

    return render(request, 'app_id_start.html', {
        'data_smp': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
        'patients': patients,
        'total_records': total_records,
        'records_per_page': records_per_page,
        'groups': user_groups_list, # Получаем все группы
        'filter_records': filter_records,  #  количество записей - отфильтрованное
        'search_fio_status': search_fio_status,  # передаем значение search_fio_status в шаблон
        'search_fio': query_fio,
        'search_id': query_id,
        'search_oms': query_oms,
    })


def v_id_edit_patient(request, id):
    patient = get_object_or_404(IdReesrtFio, id=id)

    # --------------- вычсление перес=менных по ДНЯМ!!! ------------

    if request.method == 'POST':
        # Обновляем поля, которые можно редактировать
        # ------------------- поля для редактирования и сохранения --------
        patient.fio_pacienta = request.POST.get('fio_pacienta')
        patient.data_rozhdeniya = request.POST.get('data_rozhdeniya')


        # -----Начало блока проверки даты------ получение ДАТЫ и ее проверка на пустоту!!!--------
        patient.data_rozhdeniya = request.POST.get('data_rozhdeniya')
        patient.data_rozhdeniya = zamena_pustot(patient.data_rozhdeniya)
        # ---------Конец блока проверки даты- получение ДАТЫ и ее проверка на пустоту!!!-----------

        patient.polis_oms = request.POST.get('polis_oms')
        patient.pol = request.POST.get('pol')

        # -----------------------
        if 'save' in request.POST:  # Кнопка "Сохранить"
            request.session['id_pac'] = patient.id_pac
            request.session['fio_pacienta'] = patient.fio_pacienta
            request.session['data_rozhdeniya'] = patient.data_rozhdeniya
            request.session['polis_oms'] = patient.polis_oms
            request.session['pol'] = patient.pol
            # patient.save()

            return redirect('app_id:v_id_proverka', id=patient.id)  # Переходим на страницу проверки

    return render(request, 'app_id_edit_pacient_short.html', {'patient': patient,
                                                       # 'koli4_dney_ot_proshlogo_vizita_vracha': koli4_dney_ot_proshlogo_vizita_vracha,
                                                       # 'dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover': dni_kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover,
                                                       })



def v_id_proverka(request, id):
    # patient = get_object_or_404(IdReesrtFio, id=id)
    print('22222')
    print(request.session.get('id_pac'))

    id_pac = request.session.get('id_pac')
    fio_pacienta = request.session.get('fio_pacienta')
    data_rozhdeniya = request.session.get('data_rozhdeniya')
    polis_oms = request.session.get('polis_oms')
    pol = request.session.get('pol')


    if request.method == 'POST':
        if 'vnosim_v_bazy' in request.POST:  # Кнопка "vnosim_v_bazy"
            patient = get_object_or_404(IdReesrtFio, id=id)

            patient.id_pac = id_pac
            patient.fio_pacienta = fio_pacienta
            patient.data_rozhdeniya = data_rozhdeniya
            patient.polis_oms = polis_oms
            patient.pol = pol

            patient.save()
            return redirect('app_id:v_id_add_svedeniya_o_pac')  # Переходим на главную страницу

        elif 'korrektirovat' in request.POST:  # Кнопка "Корректировать"
            return redirect('app_id:v_id_edit_patient', id=id)  # Возвращаем на страницу редактирования

    return render(request, 'app_id_proverke_pacient.html', {
                                                            # 'patient': patient,
                                                            'id_pac': id_pac,
                                                            'fio_pacienta': fio_pacienta,
                                                            'data_rozhdeniya': data_rozhdeniya,
                                                            'polis_oms': polis_oms,
                                                            'pol': pol,

                                                          })

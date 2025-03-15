# app_planfact/models.py

from django.db import models

class PlanFactTab(models.Model):


    # Поля для даты

    data_planfakta = models.DateField( blank=True, null=True)
    planovaya_data_vizita_soglasno_emias_reestru = models.DateField( blank=True, null=True)
    fakticheskaya_data_vizita_soglasno_emias = models.DateField( blank=True, null=True)
    data_rozhdeniya = models.DateField( blank=True, null=True)

    # Текстовые поля

    id_pac = models.CharField(max_length=100, null=True)
    fio_pacienta = models.CharField(max_length=250, null=True)
    polis_oms = models.CharField(max_length=250, null=True)
    ovpp_name = models.TextField( blank=True, null=True)
    vopros_dlya_razbora = models.TextField( blank=True, null=True)

    otvet_kc = models.TextField( blank=True, null=True)


    name_mo_provod_vk = models.TextField( blank=True, null=True)
    diagnoz_mkb10 = models.TextField( blank=True, null=True)

    komment_k_pervichnomu_vizitu = models.TextField( blank=True, null=True)
    komment_k_posled_vizitu                     = models.TextField( blank=True, null=True)

    tyagostnaya_simptomatika_pall_potrebnosti   = models.TextField( blank=True, null=True)
    plan_nablyudeniya_sootvestvuet_tyazhesti_sostoyaniya_i_prognozu = models.TextField( blank=True, null=True)


    vizov_smp_posle_last_vizit = models.TextField( blank=True, null=True)


    nalichie_pokazanij_k_okazaniyu_specPMP      = models.TextField( blank=True, null=True)
    nablyudenie_v_drugoj_mo_parallel_s_ovpp     = models.TextField( blank=True, null=True)

    name_drugoj_mo_parallel_s_ovpp              = models.TextField( blank=True, null=True)
    osnovaniya_parallel_nabluden = models.TextField(blank=True, null=True)

    vypiska_receptov_vps                        = models.TextField( blank=True, null=True)
    vypiska_receptov_drugoj_mo                  = models.TextField( blank=True, null=True)
    potrebnost_v_respiratorke                   = models.TextField( blank=True, null=True)
    vyvlennye_defekty                           = models.TextField( blank=True, null=True)
    mery_prinyatye_vps_dlya_uluchsheniya_pmp    = models.TextField( blank=True, null=True)
    predlozheniya_dlya_uluchsheniya_pmp         = models.TextField( blank=True, null=True)
    komment_zav_vps                             = models.TextField( blank=True, null=True)
    komment_aup                                 = models.TextField( blank=True, null=True)

    data_vk                                     = models.DateField(verbose_name='data_vk', null=True)
    data_poslednego_poseshcheniya_drugoj_mo     = models.DateField(verbose_name='data_poslednego_poseshcheniya_drugoj_mo', null=True)
    data_poslednego_vizita                      = models.DateField(verbose_name='data_poslednego_vizita', null=True)
    data_pervichnogo_vizita                     = models.DateField(verbose_name='data_pervichnogo_vizita', null=True)
    data_vklyucheniya_v_reestr                  = models.DateField(verbose_name='data_vklyucheniya_v_reestr', null=True)

    # data_last_changed_med = models.DateField(verbose_name='Дата посл.изменения мед_блока', null=True)

    ok_status_zapolnenia = models.CharField(max_length=50,blank=True, null=True) # Новое  поле для кэр






    class Meta:
        db_table = 'plan_fact_tab'  # Указываем имя таблицы в БД
    #


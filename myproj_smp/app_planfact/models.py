# app_planfact/models.py

from django.db import models

class PlanFactTab(models.Model):


    # Поля для даты

    data_planfakta = models.DateField( blank=True, null=True)
    planovaya_data_vizita_soglasno_emias_reestru = models.DateField( blank=True, null=True)
    fakticheskaya_data_vizita_soglasno_emias = models.DateField( blank=True, null=True)
    data_rozhdeniya = models.DateField( blank=True, null=True)

    # Текстовые поля


    fio_pacienta = models.CharField(max_length=250, null=True)
    polis_oms = models.CharField(max_length=250, null=True)
    ovpp_name = models.TextField( blank=True, null=True)
    vopros_dlya_razbora = models.TextField( blank=True, null=True)

    otvet_kc = models.TextField( blank=True, null=True)
    defekty_v_okazanii_pmp_na_osnovanii_karty_kontrolya_kachest = models.TextField( blank=True, null=True)
    opisanie_defektov = models.TextField(blank=True, null=True)
    vyvody_svyaz_perenosa_vizita_s_defektami_okazaniya_pmp = models.TextField( blank=True, null=True)
    vypolnennye_meropriyatiya_po_nedopushcheniyu_perenosov = models.TextField( blank=True, null=True)


    sbor_zhalob_v_polnom_obeme = models.TextField( blank=True, null=True)
    vypolnena_i_otrazhena_v_protokole_vracha_ocenka_intensivnosti = models.TextField(blank=True, null=True)
    v_pole_kommentarii_otrazhen_bolevoj_anamnez_prinimaemye_prepa = models.TextField(blank=True, null=True)
    sbor_anamneza_osnovnogo_zabolevaniya_v_polnom_obeme_otrazhena = models.TextField(blank=True, null=True)
    osmotr_pacienta_proveden_v_polnom_obeme = models.TextField(blank=True, null=True)
    polya_osmotra_pacienta_ne_protivorechat_drug_drugu = models.TextField(blank=True, null=True)
    pri_povtornom_vneplanovom_vizite_otrazhena_dinamika_sostoyani = models.TextField(blank=True, null=True)
    ustanovlennyj_diagnoz_ne_protivorechit_dannym_onkokonsiliuma = models.TextField(blank=True, null=True)
    v_oslozhneniyakh_vyneseny_diagnozy_khronicheskij_bolevoj_sin = models.TextField(blank=True, null=True)
    ocenka_tyazhesti_sostoyaniya_pacienta_sootvetstvuet_statusu = models.TextField(blank=True, null=True)
    pri_otkaze_pacienta_ot_pmp_podpisan_i_zagruzhen_v_sistemu = models.TextField(blank=True, null=True)

    pri_nalichii_pokazanij_dlya_okazaniya_pmp_v_stacionarnykh = models.TextField( blank=True, null=True)
    pri_otkaze_pacienta_ot_gospitalizacii_podpisan_i_zagruzhe = models.TextField( blank=True, null=True)
    pri_okazanii_pmp_v_ambulatornykh_usloviyakh_naznachen_pat = models.TextField( blank=True, null=True)
    patronazhnyj_plan_i_data_sleduyushchego_vizita_otrazheny = models.TextField( blank=True, null=True)
    pri_bolevom_sindrome_vypiske_receptov_otkaze_ot_gospitali = models.TextField( blank=True, null=True)
    pri_naznachenii_daty_gospitalizacii_pacienta_vizity_medi = models.TextField( blank=True, null=True)
    ukazany_planovye_daty_zameny_medicinskikh_izdelij_imeyus = models.TextField( blank=True, null=True)
    na_vizite_prinyato_reshenie_i_vypolneno_vvedenie_lekarstv = models.TextField( blank=True, null=True)
    v_rekomendaciyakh_k_osmotru_ukazany_vse_naznachennye_leka = models.TextField( blank=True, null=True)

 # 'pacientu_vypolneny_naznacheniya_lekarstvennykh_preparatov'
    pacientu_vypolneny_naznacheniya_lekarstvennykh_preparatov = models.TextField(blank=True, null=True)
    vypisany_recepturnye_blanki_na_naznachennye_lekarstvennye = models.TextField( blank=True, null=True)
    pri_usilenii_bolevogo_sindroma_i_drugoj_tyagostnoj_simpto = models.TextField( blank=True, null=True)
    obezbolivayushchie_preparaty_dlya_regulyarnogo_priema_naz = models.TextField( blank=True, null=True)

    opisanie_defektov_33 = models.TextField(blank=True, null=True)
    naznacheny_lekarstvennye_preparaty_dlya_profilaktiki_i_ku = models.TextField( blank=True, null=True)
    pacient_lico_osushchestvlyayushchee_ukhod_oznakomleny_s_p = models.TextField( blank=True, null=True)
    pri_nalichii_pokazanij_dlya_gospitalizacii_v_protokole_vr = models.TextField( blank=True, null=True)
    palliativnaya_pomoshch_okazana_svoevremenno_i_v_polnom_ob = models.TextField( blank=True, null=True)
    patronazhnyj_plan_naznachen_v_sootvetstvii_so_statusom_pa = models.TextField( blank=True, null=True)
    gospitalizaciya_pacienta_v_stacionarnye_palliativnye_otde = models.TextField( blank=True, null=True)
    ehffektivnyj_podbor_i_korrekciya_simptomaticheskoj_terapi = models.TextField( blank=True, null=True)
    vyyavleny_defekty_okazaniya_palliativnoj_pomoshchi_kotory = models.TextField( blank=True, null=True)
    provedennye_meropriyatiya = models.TextField( blank=True, null=True)


    ok_status_zapolnenia = models.CharField(max_length=50,blank=True, null=True) # Новое  поле для кэр

    class Meta:
        db_table = 'plan_fact_tab'  # Указываем имя таблицы в БД
    #
    # def __str__(self):
    #     return self.name


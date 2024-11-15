from django.db import models

class SmpRazborTab(models.Model):
    # Текстовые поля
    fio_pacienta = models.CharField(max_length=250, null=True)
    rezultat_vyzova = models.TextField( blank=True, null=True)
    aktiv_passiv = models.CharField(max_length=255, blank=True, null=True)
    diagnoz_po_mkb = models.CharField(max_length=255, blank=True, null=True)
    prichina_vyzova_skoroiy_pomoschi = models.TextField( blank=True, null=True)
    nalichie_bolevogo_sindroma = models.CharField(max_length=255, blank=True, null=True)
    prichina_vyzova_skoroiy_pomoschi_kratko = models.TextField( blank=True, null=True)
    kuriruyushchee_podrazdelenie_ovpp = models.CharField(max_length=255, blank=True, null=True)
    dejstviya_cpp = models.TextField( blank=True, null=True)
    byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite = models.CharField(max_length=255, blank=True, null=True)
    otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme = models.CharField(max_length=255, blank=True, null=True)
    dinamika_sostoyaniya = models.CharField(max_length=255, blank=True, null=True)
    fio_vracha = models.CharField(max_length=255, blank=True, null=True)
    sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle = models.CharField(max_length=255, blank=True, null=True)
    kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij = models.CharField(max_length=255, blank=True, null=True)


    vyvod = models.TextField( blank=True, null=True)


    kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya = models.TextField( blank=True, null=True)
    kakie_dejstviya_byli_predprinyaty_smp = models.TextField( blank=True, null=True)
    tekushchee_sostoyanie_pacienta_posle_vyzova_smp = models.TextField( blank=True, null=True)
    ostalis_li_zhaloby_posle_vyzova_smp = models.CharField(max_length=255, blank=True, null=True)
    opisanie_zhalob = models.TextField( blank=True, null=True)
    byli_li_lekarstvennye_sredstva_otovareny_po_receptu = models.TextField( blank=True, null=True)
    pacient_prinimaet_naznachennye_lekarstvennye_sredstva = models.CharField(max_length=255, blank=True, null=True)
    ehffektivna_li_naznachennaya_medikamentoznaya_terapiya = models.CharField(max_length=255, blank=True, null=True)
    est_li_pobochnye_dejstviya_ot_naznachennykh_lekarstvennykh = models.CharField(max_length=255, blank=True, null=True)
    pacientu_byla_ozvuchena_data_sleduyushchego_vizita = models.CharField(max_length=255, blank=True, null=True)
    pacientu_byli_predostavleny_kontaktnye_nomera_cpp = models.CharField(max_length=255, blank=True, null=True)
    pacient_zvonil_po_ukazannym_kontaktnym_nomera_do_vyzova_smp = models.CharField(max_length=255, blank=True, null=True)
    prichina_po_kotoroj_pacient_ne_zvonil_po_ukazannym_nomeram = models.TextField( blank=True, null=True)
    sootvetstvuet_li_naznachennyj_bazovyj_plan_sostoyaniyu_pacie = models.CharField(max_length=255, blank=True, null=True)
    trebovanie_gospitalizacii_na_dannyj_moment = models.CharField(max_length=255, blank=True, null=True)
    bazovyj_plan_naznachen_korrektno = models.CharField(max_length=255, blank=True, null=True)
    ocenka_sostoyaniya_sootvetstvuet_bazovomu_planu = models.CharField(max_length=255, blank=True, null=True)
    zhaloby_opisany_v_polnom_obeme = models.CharField(max_length=255, blank=True, null=True)
    ocenka_zaveduyushchego_proizvedena_korrektno = models.CharField(max_length=255, blank=True, null=True)
    vyvody_po_rezultatm_ocenki = models.TextField( blank=True, null=True)
    vyyavlennye_defekty_v_rabote_vracha = models.TextField( blank=True, null=True)
    ocenka_dejstvij_vracha_do_vyzova_smp = models.TextField( blank=True, null=True)
    ocenka_dejstvij_posle_vyzova_smp = models.TextField( blank=True, null=True)
    analiz_dejstvij_glavnym_vrachom = models.TextField( blank=True, null=True)
    polis_oms = models.CharField(max_length=255, blank=True, null=True)
    # -37

    # Целочисленные поля
    p_p = models.IntegerField( blank=True, null=True)
    kolichestvo_vyezdov_v_den = models.IntegerField( blank=True, null=True)
    kolichestvo_dnej_ot_momenta_polucheniya_dannykh_po_smp_do_sover = models.IntegerField( blank=True, null=True)
    kolichestvo_dnej_ot_proshlogo_vizita_vracha = models.IntegerField( blank=True, null=True)

    # Поля для даты
    kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu = models.DateField(blank=True, null=True)
    data_poslednego_vizita_vracha_iz_protokola_osmotra_emias = models.DateField( blank=True, null=True)
    data_naznachenogo_audioprotokola_soglasno_protokolu_v  = models.DateField( blank=True, null=True)
    data_polucheniya_svedenij_po_vyzovam_smp_ot_kc  = models.DateField( blank=True, null=True)
    data_audioprotokola_posle_polucheniya_dannykh_o_vyzove_smp  = models.DateField( blank=True, null=True)
    data_vyzova_smp = models.DateField( blank=True, null=True)
    data_rozhdeniya = models.DateField( blank=True, null=True)
    data_vklyucheniya_v_registr = models.DateField( blank=True, null=True)

    ok_vps = models.CharField(max_length=100) # Новое  поле для кэр

    class Meta:
        db_table = 'smp_razbor_tab'  # Указываем имя таблицы в БД
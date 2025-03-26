from django.db import models

class KisLong(models.Model):

    n_istorii_bolezni = models.CharField(max_length=255, verbose_name='№ истории болезни',null=True)
    fio_pacienta = models.CharField(max_length=255, verbose_name='ФИО',null=True)
    otdelenie = models.CharField(max_length=255, verbose_name='отделение',null=True)
    kojko_dni = models.IntegerField(verbose_name='койко_дни',null=True)
    # diagnoz_osnovnoj = models.CharField(max_length=255, verbose_name='Диагноз основной',null=True)
    ppi = models.CharField(max_length=255, verbose_name='ppi',null=True)

    # medic_kriterii = models.CharField(max_length=355, verbose_name='medic_kriterii', null=True)

    dinamika_sostoyania = models.CharField(max_length=255, verbose_name='dinamika_sostoyania', null=True)

    dvigatel_activnost = models.CharField(max_length=255, verbose_name='dvigatel_activnost', null=True)
    potrebnost_v_soc_koordinat = models.CharField(max_length=255, verbose_name='potrebnost_v_soc_koordinat', null=True)
    status_med_karty = models.CharField(max_length=255, verbose_name='status_med_karty', null=True)
    status_po_mse = models.CharField(max_length=255, verbose_name='status_po_mse', null=True)
    status_nabludeniya = models.CharField(max_length=255, verbose_name='status_nabludeniya', null=True)
    med_pokazaniya = models.CharField(max_length=255, verbose_name='med_pokazaniya', null=True)

    soc_kriterii = models.CharField(max_length=255, verbose_name='soc_kriterii',null=True)
    funkciional_kriterii = models.CharField(max_length=255, verbose_name='funkciional_kriterii',null=True)
    # psikh_kriterii = models.CharField(max_length=255, verbose_name='psikh_kriterii',null=True)
    # org_kriterii = models.CharField(max_length=255, verbose_name='org_kriterii',null=True)
    # nalichie_zayavki_v_soc_sluzhbu = models.CharField(max_length=255, verbose_name='nalichie_zayavki_v_soc_sluzhbu',null=True)

    # prichna_otsutstviya_zayavki = models.CharField(max_length=255, verbose_name='prichna_otsutstviya_zayavki',null=True)
    kommentarij = models.TextField( verbose_name='kommentarij',null=True)
    iskhod_gospit = models.CharField(max_length=255, verbose_name='iskhod_gospit',null=True)
    tema_zayavki_pomosh_v_zhizneustrojstve = models.TextField(verbose_name='tema_zayavki_pomosh_v_zhizneustrojstve',null=True)
    nalichie_rodstvennikov = models.TextField( verbose_name='nalichie_rodstvennikov',null=True)
    fio_zaveduyushchego_otd = models.CharField(max_length=255, verbose_name='fio_zaveduyushchego_otd',null=True)
    fio_lechashchego_vracha = models.CharField(max_length=255, verbose_name='fio_lechashchego_vracha',null=True)
    # kommentarij_soc = models.TextField( verbose_name='kommentarij_soc',null=True)
    status_pacienta = models.CharField(max_length=255, verbose_name='status_pacienta',null=True) # - статус решения о переводе
    soc_koordinator = models.CharField(max_length=255, verbose_name='soc_koordinator',null=True)
    kommentarij_soc_koordinatorov_dtszn = models.TextField( verbose_name='kommentarij_soc_koordinatorov_dtszn',null=True)

    # reshenie_po_pacientu = models.TextField( verbose_name='reshenie_po_pacientu',null=True)

    pacient_ne_mozhet_vyrazit_svoe_soglasie = models.CharField(max_length=255, verbose_name='pacient_ne_mozhet_vyrazit_svoe_soglasie',null=True)

    # status_zapisi = models.CharField(max_length=255, verbose_name='status_zapisi',null=True)

    data_rozhdeniya = models.DateField(verbose_name='Дата рождения',null=True)
    data_gospit = models.DateField(verbose_name='Дата госпитализации',null=True)
    data_vypiski = models.DateField(verbose_name='Дата выписки',null=True)
    data_peredachi_soc_koordinatoram_dtszn = models.DateField( verbose_name='data_peredachi_soc_koordinatoram_dtszn',null=True)
    data_prinyatiya_v_rabotu_soc_koordinatorami_dtszn = models.DateField(verbose_name='Дата принятия в работу',null=True)
    # data_prinyatiya_resheniya_po_pacientu = models.DateField(verbose_name='Дата статуса решения о переводе',null=True)
    data_resheniya_dtszn = models.DateField(verbose_name='Дата решения ДТСЗН',null=True)

    data_last_changed_med = models.DateField(verbose_name='Дата посл.изменения мед_блока',null=True)
    data_last_changed_soc = models.DateField(verbose_name='Дата посл.изменения соц_блока',null=True)

    # otkaz_rodstvennikov = models.CharField(max_length=255, verbose_name='otkaz_rodstvennikov',null=True)
    sposoben_virazit_soglasie = models.CharField(max_length=50, verbose_name='sposoben_virazit_soglasie',null=True)
    reshenie_dtszn_po_putevke = models.CharField(max_length=255, verbose_name='soc_koordinator', null=True)
    poyasneniya_k_resheniyu_po_pac = models.TextField(verbose_name='reshenie_po_pacientu', null=True)
    status_resheniya_o_perevode = models.TextField(verbose_name='status_resheniya_o_perevode', null=True)

    poluchatel_soc_uslug = models.CharField(max_length=50, verbose_name='poluchatel_soc_uslug',null=True)

    svedeniya_o_pac_peredani_dtszn = models.CharField(max_length=255, verbose_name='svedeniya_o_pac_peredani_dtszn', null=True)
    data_peredachi_sveden_v_dtszn = models.DateField(verbose_name='data_peredachi_sveden_v_dtszn',  null=True)

    class Meta:
        db_table = 'kis_long_tab'  # Указываем имя таблицы в БД

class KisChange(models.Model):

    id_pacienta = models.IntegerField(verbose_name='id_pacienta', null=True)
    fio_pacienta = models.CharField(max_length=355, verbose_name='fio_pacienta', null=True)
    name_changed_colon = models.CharField(max_length=255, verbose_name='name_changed_colon', null=True)
    data_old = models.TextField(verbose_name='reshenie_po_pacientu', null=True)
    data_new = models.TextField(verbose_name='reshenie_po_pacientu', null=True)
    time_changed = models.CharField(max_length=255, verbose_name='data_new', null=True)
    who_changed = models.CharField(max_length=255, verbose_name='data_new', null=True)
    # time_changed = models.DateTimeField( verbose_name='time_changed',null=True)

    class Meta:
        db_table = 'kis_change_tab'  # Указываем имя таблицы в БД


class Kis(models.Model):
    pacient = models.TextField( verbose_name='pacient',null=True)
    snils = models.CharField(max_length=250, verbose_name='snils',null=True)
    adres_region = models.TextField( verbose_name='adres_region',null=True)
    adres = models.TextField( verbose_name='adres',null=True)
    grazhdanstvo = models.CharField(max_length=255, verbose_name='grazhdanstvo',null=True)
    soc_status = models.CharField(max_length=255, verbose_name='soc_status',null=True)
    otdelenie_name = models.CharField(max_length=255, verbose_name='otdelenie_id',null=True)
    ishod = models.CharField(max_length=255, verbose_name='ishod',null=True)
    telefon = models.CharField(max_length=255, verbose_name='telefon',null=True)
    kont_inf = models.TextField( verbose_name='kont_inf',null=True)
    ib_nomer = models.CharField(max_length=255, verbose_name='ib_nomer', null=True)
    ib_god= models.CharField(max_length=255, verbose_name='ib_god', null=True)
    diagnoz_osn = models.TextField( verbose_name='diagnoz_osn',null=True)
    diagnoz_napr_mu = models.TextField( verbose_name='diagnoz_napr_mu',null=True)
    dyl = models.TextField( verbose_name='dyl',null=True)

    data_rozhd = models.DateField( verbose_name='data_rozhd',null=True)
    data_gospit = models.DateField(verbose_name='data_gospit', null=True)
    data_vipiski = models.DateField(verbose_name='data_vipiski', null=True)

    class Meta:
        db_table = 'kis_tab'  # Указываем имя таблицы в БД
from django.db import models

# Create your models here.
class Uborka(models.Model):

    ub_oborudovanie_name = models.CharField(max_length=255, verbose_name='ub_oborudovanie_name',null=True)
    ub_inventarnik = models.CharField(max_length=255, verbose_name='ub_inventarnik',null=True)
    ub_fio_mol = models.CharField(max_length=255, verbose_name='ub_fio_mol',null=True)
    ub_fio_pacienta = models.CharField(max_length=255, verbose_name='ub_fio_pacienta',null=True)
    ub_data_rozhdeniya = models.DateField(verbose_name='ub_data_rozhdeniya', null=True)

    ub_grazhdanstvo = models.CharField(max_length=255, verbose_name='ub_grazhdanstvo',null=True)

    ub_tip_dvizheniya = models.CharField(max_length=255, verbose_name='ub_tip_dvizheniya',null=True)
    ub_tekushiy_status_pac = models.CharField(max_length=255, verbose_name='ub_tekushiy_status_pac',null=True)

    ub_filial_vps = models.CharField(max_length=255, verbose_name='ub_filial_vps',null=True)
    ub_svedeniya_mol = models.CharField(max_length=255, verbose_name='ub_svedeniya_mol',null=True)
    ub_location_pac = models.TextField( verbose_name='ub_location_pac',null=True)
    ub_kommentarij = models.TextField( verbose_name='kommentarij',null=True)
    ub_kommentarij_yur = models.TextField( verbose_name='ub_kommentarij_yur',null=True)

    ub_priznak_archiv = models.TextField( verbose_name='ub_priznak_archiv',null=True)


    ub_data_izmeneniy                        = models.DateField(verbose_name='ub_data_izmeneniy', null=True)
    ub_data_archiv                           = models.DateField(verbose_name='ub_data_archiv', null=True)
    ub_reshenie_yur                     = models.CharField(max_length=255, verbose_name='ub_svedeniya_mol',null=True)


    class Meta:
        db_table = 'uborka_tab'  # Указываем имя таблицы в БД


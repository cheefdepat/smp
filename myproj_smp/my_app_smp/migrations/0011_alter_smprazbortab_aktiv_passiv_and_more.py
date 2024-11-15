# Generated by Django 5.1.3 on 2024-11-13 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app_smp', '0010_alter_smprazbortab_rezultat_vyzova'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smprazbortab',
            name='aktiv_passiv',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='bazovyj_plan_naznachen_korrektno',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='byl_li_ustanovlen_bazovyj_plan_na_poslednem_vizite',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='dejstviya_cpp',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='diagnoz_po_mkb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='dinamika_sostoyaniya',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='ehffektivna_li_naznachennaya_medikamentoznaya_terapiya',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='est_li_pobochnye_dejstviya_ot_naznachennykh_lekarstvennykh',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='fio_pacienta',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='fio_vracha',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='kontrol_ispolneniya_naznachennykh_vrachom_cpp_rekomendacij',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='kuriruyushchee_podrazdelenie_ovpp',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='nalichie_bolevogo_sindroma',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='ocenka_sostoyaniya_sootvetstvuet_bazovomu_planu',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='ocenka_zaveduyushchego_proizvedena_korrektno',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='ostalis_li_zhaloby_posle_vyzova_smp',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='otobrazheny_li_vse_zhaloby_pacienta_v_polnom_obeme',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='pacient_prinimaet_naznachennye_lekarstvennye_sredstva',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='pacient_zvonil_po_ukazannym_kontaktnym_nomera_do_vyzova_smp',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='pacientu_byla_ozvuchena_data_sleduyushchego_vizita',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='pacientu_byli_predostavleny_kontaktnye_nomera_cpp',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='prichina_vyzova_skoroiy_pomoschi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='prichina_vyzova_skoroiy_pomoschi_kratko',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='rezultat_vyzova',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='sootvetstvuet_li_naznachennyj_bazovyj_plan_sostoyaniyu_pacie',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='sravnenie_povoda_vyz_smp_s_prot_vracha_cpp_do_i_posle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='trebovanie_gospitalizacii_na_dannyj_moment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='vyvod',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='zhaloby_opisany_v_polnom_obeme',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

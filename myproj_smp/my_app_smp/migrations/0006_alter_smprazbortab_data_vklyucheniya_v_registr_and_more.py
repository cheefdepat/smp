# Generated by Django 5.1.3 on 2024-11-13 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app_smp', '0005_alter_smprazbortab_aktiv_passiv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smprazbortab',
            name='data_vklyucheniya_v_registr',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='smprazbortab',
            name='vyyavlennye_defekty_v_rabote_vracha',
            field=models.TextField(blank=True, null=True),
        ),
    ]
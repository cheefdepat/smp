from django.db import models

class KisLong(models.Model):
    FIO_pac = models.CharField(max_length=255, verbose_name='ФИО пациента')
    date_birth = models.DateField(verbose_name='Дата рождения')
    date_hosp = models.DateField(verbose_name='Дата госпитализации')

    def __str__(self):
        return self.FIO_pac
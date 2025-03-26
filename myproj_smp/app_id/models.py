from django.db import models

class IdReesrtFio(models.Model):


    # Поля для даты

    data_rozhdeniya = models.DateField( blank=True, null=True)

    # Текстовые поля

    id_pac = models.CharField(max_length=100, null=True)
    fio_pacienta = models.CharField(max_length=250, null=True)
    polis_oms = models.CharField(max_length=250, null=True)
    pol = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'id_reesrt_tab'  # Указываем имя таблицы в БД


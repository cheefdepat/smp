from django import forms
from .models import KisLong

class KisLongForm(forms.ModelForm):
    class Meta:
        model = KisLong
        fields = (
            'fio_pacienta',
            'data_rozhdeniya',
            'otdelenie',
            'data_gospit',
            'kojko_dni',
            'status_pacienta',
            'sostoyanie_zayavki',

            )

class KisLongFormСhoiceMedKriter(forms.Form):
    class Meta:
        model = KisLong  # Укажите вашу модель
        # fields = '__all__'  # Включить все поля модели
        fields = ['medic_kriterii']


class KisLongFilterForm(forms.Form):
    fio_pacienta = forms.CharField(label='ФИО', required=False)
    otdelenie = forms.CharField(label='Отделение', required=False)
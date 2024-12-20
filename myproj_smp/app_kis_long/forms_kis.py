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
    fio_pacienta = forms.CharField(label='ФИО',
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'style': 'width: 350px; background-color: #87CEEB;'})
                                   )
    otdelenie = forms.CharField(label='Отделение',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    kojko_dni_min = forms.IntegerField(label='Количество дней (мин.)',
                                       required=False,
                                       # initial=1,
                                       widget=forms.NumberInput(
                                              attrs={'style': 'width: 50px; background-color: #87CEEB;'}))
    kojko_dni_max = forms.IntegerField(label='Количество дней (макс.)',
                                       required=False,
                                       # initial=3000,
                                       widget=forms.NumberInput(
                                               attrs={'style': 'width: 50px; background-color: #87CEEB;'}))
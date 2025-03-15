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
            # 'sostoyanie_zayavki',

            )

class KisLongFormСhoiceMedKriter(forms.Form):
    class Meta:
        model = KisLong  # Укажите вашу модель
        # fields = '__all__'  # Включить все поля модели
        fields = ['medic_kriterii']


class KisLongFilterForm(forms.Form):
    form_fio_pacienta = forms.CharField(label='ФИО',
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'style': 'width: 350px; background-color: #87CEEB;'})
                                   )
    form_otdelenie = forms.CharField(label='Отделение',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 250px; background-color: #87CEEB;'})
                                 )

    form_iskhod_gospit = forms.ChoiceField(label='Исход госпитализации',
                                          required=False,
                                          choices=[
                                              ('', 'Все'),
                                              ('Пациент в стационаре', 'Пациент в стационаре'),
                                              ('1. Выписан домой', '1. Выписан домой'),
                                              ('2. Выписан в соц.учреждение', '2. Выписан в соц.учреждение'),
                                              ('3. Переведен в другое ЛПУ', '3. Переведен в другое ЛПУ'),
                                              ('4. Умер в стационаре', '4. Умер в стационаре'),
                                          ],
                                          initial='Пациент в стационаре',  # Установите значение по умолчанию
                                          widget=forms.Select(
                                              attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                          )


    form_kojko_dni_min = forms.IntegerField(label='Количество дней (мин.)',
                                       required=False,
                                       # initial=1,
                                       widget=forms.NumberInput(
                                              attrs={'style': 'width: 50px; background-color: #87CEEB;'}))
    # form_kojko_dni_max = forms.IntegerField(label='Количество дней (макс.)',
    #                                    required=False,
    #                                    # initial=3000,
    #                                    widget=forms.NumberInput(
    #                                            attrs={'style': 'width: 50px; background-color: #87CEEB;'}))

    form_med_pokazaniya = forms.ChoiceField(label='Мед.показания',
                                           required=False,
                                           choices=[
                                               ('', 'Все'),
                               ('0. Мед.показания отсутствуют', '0.Мед.показания отсутствуют'),
                               ('1. Тяжелая одышка 5-7 баллов+', '1.Тяжелая одышка 5-7 баллов+'),
                               ('2. Дисфагия 3-4 ст.', '2.Дисфагия 3-4ст.'),
                               ('3. Эметический некупируемый синдром', '3.Эметический некупируемый синдром'),
                               ('4. Нарастающий отек, асцит или плевральный выпот(треб.дренирование)', '4.Нарастающий отек,асцит/плевральный выпот'),
                               ('5. Пролежни/трофические язвы(III-IVст.), ежеднев.обработки', '5.Пролежни/трофические язвы(III-IVст.)'),
                               ('6. Стомы, катетеры, осложненное течение', '6. Стомы, катетеры, осложненное течение'),
                               ('7. Выраженный болевой синдром, требующий коррекции', '7. Выраженный болевой синдром, требующий коррекции '),

                                           ],
                                           initial='Все',  # Установите значение по умолчанию
                                           widget=forms.Select(
                                               attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                           )

    form_potrebnost_v_soc = forms.ChoiceField(label='Потребность в соц.',
                                           required=False,
                                           choices=[
                                               ('', 'Все'),
                               ('1. Нет потребности в соц.координаторе', '1.Нет потребности в соц.координаторе'),
                               ('2. Есть потребность в соц.координаторе', '2.Есть потребность в соц.координаторе'),
                                              ],
                                           initial='Все',  # Установите значение по умолчанию
                                           widget=forms.Select(
                                               attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                           )


class KisFilterForm(forms.Form):
    form_fio_pacienta = forms.CharField(label='ФИО',
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'style': 'width: 350px; background-color: #87CEEB;'})
                                   )
    form_otdelenie = forms.CharField(label='Отделение',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    form_kojko_dni_min = forms.IntegerField(label='Количество дней (мин.)',
                                       required=False,
                                       initial=60,  # Устанавливаем значение по умолчанию
                                       widget=forms.NumberInput(
                                              attrs={'style': 'width: 50px; background-color: #87CEEB;'}))
    # form_kojko_dni_max = forms.IntegerField(label='Количество дней (макс.)',
    #                                    required=False,
    #                                    # initial=3000,
    #                                    widget=forms.NumberInput(
    #                                            attrs={'style': 'width: 50px; background-color: #87CEEB;'}))
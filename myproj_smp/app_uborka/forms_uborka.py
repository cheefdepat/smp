from django import forms
from .models import Uborka



class UborkaFilters(forms.Form):
    form_oborudovanie_name = forms.CharField(label='form_oborudovanie_name',
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'style': 'width: 350px; background-color: #87CEEB;'})
                                   )
    form_inventarnik = forms.CharField(label='form_inventarnik',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    form_fio_mol = forms.CharField(label='form_fio_mol',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    form_fio_pacienta = forms.CharField(label='form_fio_pacienta',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    form_tekushiy_status_pac = forms.CharField(label='form_tekushiy_status_pac',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )

    form_filial_vps = forms.CharField(label='form_filial_vps',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'style': 'width: 150px; background-color: #87CEEB;'})
                                 )


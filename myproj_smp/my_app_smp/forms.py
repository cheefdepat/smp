from django import forms
from .models import SmpRazborTab
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import User

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class SmpRazborTabForm(forms.ModelForm):
    class Meta:
        model = SmpRazborTab
        fields = [
            'kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya',
            'vyvody_po_rezultatm_ocenki',
            'zhaloby_opisany_v_polnom_obeme',
        ]
        widgets = {
            'kakova_prichina_vyzova_smp_po_rezutatam_audiokontrolya': forms.TextInput(attrs={'class': 'form-control'}),
            'vyvody_po_rezultatm_ocenki': forms.TextInput(attrs={'class': 'form-control'}),
            'zhaloby_opisany_v_polnom_obeme': forms.TextInput(attrs={'class': 'form-control'}),
            'kakaya_data_sleduyushchego_vizita_vracha_soglasno_protokolu': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}),
        }

    # widgets = {
    #     'fio_pacienta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО', 'readonly': 'readonly'}),
    #     'rezultat_vyzova': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите результат вызова', 'readonly': 'readonly'}),
    #     'diagnoz_po_mkb': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите диагноз по МКБ'}),
    #     'prichina_vyzova_skoroiy_pomoschi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите причину вызова скорой помощи'}),
    #     'nalichie_bolevogo_sindroma': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    #     'prichina_vyzova_skoroiy_pomoschi_kratko': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите причину вызова скорой помощи кратко'}),
    #     'kuriruyushchee_podrazdelenie_ovpp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите курирующее подразделение'}),
    #     'vyyavlennye_defekty_v_rabote_vracha': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите выявленные дефекты в работе врача0'}),
    #     'data_vklyucheniya_v_registr': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату включения в регистр'}),
    # }


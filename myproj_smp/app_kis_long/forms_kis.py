from django import forms
from .models import KisLong

class KisLongForm(forms.ModelForm):
    class Meta:
        model = KisLong
        fields = ('n_istorii_bolezni', 'fio_pacienta', 'otdelenie', 'data_gospit')
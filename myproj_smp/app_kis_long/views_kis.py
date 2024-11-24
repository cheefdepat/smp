from django.shortcuts import render
from .models import KisLong
from .forms_kis import KisLongForm

def v_kis_home(request):
    if request.method == 'GET':
        patients = KisLong.objects.all()
        form = KisLongForm()
        return render(request, 'kis_long_home.html',
                      {'patients': patients, 'form': form})
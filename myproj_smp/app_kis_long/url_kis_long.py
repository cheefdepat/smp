from django.urls import path
from .views_kis import kis_patient_list


app_name = 'app_kis_long'  # Убедитесь, что это указано

urlpatterns = [
    path('', kis_patient_list, name='kis_patient_list'),


]
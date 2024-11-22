from django.urls import path
from .views_plf import plf_start_list
from .views_plf import plf_edit_patient
from .views_plf import plf_proverka_to_ker

from django.contrib.auth.decorators import login_required

# from .views import MyprojectLogout
    # edit_record  # Импортируйте ваше новое представление

app_name = 'app_planfact'  # Убедитесь, что это указано

urlpatterns = [
    path('', plf_start_list, name='plf_start_list'),
    path('plf_edit_patient/<int:id>/', plf_edit_patient, name='plf_edit_patient'),  # Новый маршрут для редактирования
    path('plf_proverka_to_ker/<int:id>/', plf_proverka_to_ker, name='plf_proverka_to_ker'),  # Новый маршрут для редактирования




]
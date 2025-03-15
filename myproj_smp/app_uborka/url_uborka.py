from django.urls import path
from .views_uborka import v_start_uborka
from .views_uborka import v_uborka_detals

from django.contrib.auth.decorators import login_required

# from .views import MyprojectLogout
    # edit_record  # Импортируйте ваше новое представление

app_name = 'app_uborka'  # Убедитесь, что это указано

urlpatterns = [
    path('', v_start_uborka, name='v_start_uborka'),
    path('v_uborka_detals/<int:id>/', v_uborka_detals, name='v_uborka_detals'),  # Новый маршрут для редактирования
    # path('plf_edit_patient/<int:id>/', plf_edit_patient, name='plf_edit_patient'),  # Новый маршрут для редактирования
    # path('plf_proverka_to_ker/<int:id>/', plf_proverka_to_ker, name='plf_proverka_to_ker'),  # Новый маршрут для редактирования
    # path('plf_export_to_excel/', plf_export_to_excel, name='plf_export_to_excel'),  # Новый маршрут для редактирования


]
from django.urls import path
from .views_kis import v_kis_home
from .views_kis import v_kis_pac_detail
from .views_kis import v_kis_pravka_kriterij
from .views_kis import run_calculate_koiko_dni
from .views_kis import v_kis_pravka_zayavka
from .views_kis import v_find_new_in_kis


app_name = 'app_kis_long'  # Убедитесь, что это указано

urlpatterns = [
    path('run-calculate-koiko-dni/', run_calculate_koiko_dni, name='run_calculate_koiko_dni'),
    path('kis/', v_kis_home, name='v_kis_home'),
    path('v_kis_pac_detail/<int:id>/', v_kis_pac_detail, name='v_kis_pac_detail'),
    path('v_kis_pravka_kriterij/<int:id>/', v_kis_pravka_kriterij, name='v_kis_pravka_kriterij'),
    path('run-v_kis_pravka_zayavka/<int:id>/', v_kis_pravka_zayavka, name='v_kis_pravka_zayavka'),
    path('v_find_new_in_kis/', v_find_new_in_kis, name='v_find_new_in_kis'),

]
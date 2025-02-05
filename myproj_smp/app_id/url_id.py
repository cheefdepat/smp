from django.urls import path
from .views_id import v_id_add_svedeniya_o_pac
from .views_id import v_id_edit_patient
from .views_id import v_id_proverka



app_name = 'app_id'  # Убедитесь, что это указано

urlpatterns = [
    path('', v_id_add_svedeniya_o_pac, name='v_id_add_svedeniya_o_pac'),
    path('v_id_edit_patient/<int:id>/', v_id_edit_patient, name='v_id_edit_patient'),  # Новый маршрут для редактирования
    path('v_id_proverka/<int:id>/', v_id_proverka, name='v_id_proverka'),  # Новый маршрут для редактирования

]
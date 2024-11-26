from django.urls import path
from .views_kis import v_kis_home


app_name = 'app_kis_long'  # Убедитесь, что это указано

urlpatterns = [
    path('kis/', v_kis_home, name='v_kis_home'),


]
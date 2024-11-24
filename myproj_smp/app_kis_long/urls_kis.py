from django.urls import path
from .views_kis import v_kis_home

from django.contrib.auth.decorators import login_required

# from .views import MyprojectLogout
    # edit_record  # Импортируйте ваше новое представление

app_name = 'app_kis_long'  # Убедитесь, что это указано

urlpatterns = [
    path('kis', v_kis_home, name='v_kis_home'),


]
from django.urls import path
from .views import home
from .views import patient_detail
from .views import edit_patient
from .views import login, logout
from .views import edit_ker
from .views import send_to_ker
from django.contrib.auth.decorators import login_required

# from .views import MyprojectLogout
    # edit_record  # Импортируйте ваше новое представление

urlpatterns = [
    path('', home, name='home'),
    path('edit/<int:id>/', edit_patient, name='edit_patient'),  # Новый маршрут для редактирования

    path('patient/<int:id>/', patient_detail, name='patient_detail'),  # Новый маршрут для деталей пациента
    path('login/', login, name='login'),  # авторизац
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),# выход
    #     ------- logout-----
    path('logout/', logout, name='logout'),
    path('edit_ker/<int:id>/', edit_ker, name='edit_ker'),
    path('edit_ker/<int:id>/', edit_ker, name='edit_ker'),
    path('send_to_ker/<int:id>/', send_to_ker, name='send_to_ker'),
]
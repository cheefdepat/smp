from django.urls import path
from .views import home
from .views import patient_detail
from .views import edit_patient
from .views import login_view, logout
from .views import edit_ker
# from .views import send_to_ker
from .views import proverka
from .views import proverka_ker
from .views import edit_glav
from .views import proverka_glav
from .views import help
from .views import start_page
# from .views import kis_patient_list
from .views import login_view
from django.conf.urls import handler404, handler500

app_name = 'my_app_smp'  # Убедитесь, что это указано


urlpatterns = [
    path('', login_view, name='login'),
    path('start/', start_page, name='start_page'),
    path('home/', home, name='home'),
    # path('kis_patient_list/', kis_patient_list, name='kis_patient_list'),
    path('edit/<int:id>/', edit_patient, name='edit_patient'),  # Новый маршрут для редактирования
    path('patient/<int:id>/', patient_detail, name='patient_detail'),  # Новый маршрут для деталей пациента


    #     ------- logout-----
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),# выход
    path('logout/', logout, name='logout'),
    path('edit_ker/<int:id>/', edit_ker, name='edit_ker'),
    path('edit_glav/<int:id>/', edit_glav, name='edit_glav'),
    path('proverka/<int:id>/', proverka, name='proverka'),
    path('proverka_ker/<int:id>/', proverka_ker, name='proverka_ker'),
    path('proverka_glav/<int:id>/', proverka_glav, name='proverka_glav'),
    path('help', help, name='help'),



]
handler404 = 'my_app_smp.views.custom_404_view'
handler500 = 'my_app_smp.views.custom_500_view'
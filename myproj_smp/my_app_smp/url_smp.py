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
from .views import results
from .views import results_page_1
from .views import results_page_2
from .views import export_to_excel
from .views import export_to_excel_for_ker
from .views import ny


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
    path('export_to_excel/', export_to_excel, name='export_to_excel'),  # вывод в Эксель
    path('export_to_excel_for_ker/', export_to_excel_for_ker, name='export_to_excel_for_ker'),  # вывод в Эксель

    path('results', results, name='results'),
    path('results_page_1/', results_page_1, name='results_page_1'),  # Добавьте этот путь
    path('results_page_2/', results_page_2, name='results_page_2'),  # Добавьте этот путь

    path('ny/', ny, name='ny'),  # Дny

]

handler404 = 'my_app_smp.views.custom_404_view'
handler500 = 'my_app_smp.views.custom_500_view'
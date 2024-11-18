"""
URL configuration for myproj_smp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from my_app_smp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('my_app_smp.url_smp')),  # Подключаем маршруты приложения
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),   ###### 3
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='login') ###### 3
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.login_view, name='login'),  # Предполагается, что у вас есть представление для входа

]
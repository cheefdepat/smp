"""
Django settings for myproj_smp project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kiytz94(_7#$gy*tl8f)q=oir-rcb-u9ra-@h%v#71c#3mpbhw'

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = [
    '172.27.216.66',
    '127.0.0.1',
    '10.159.105.227',
    '*',
    '0.0.0.0'

]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'app_smp',
    'my_app_smp',
    'app_planfact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproj_smp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproj_smp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
# ----------------------------mysql
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mysql_smp',
#         'USER': 'cheef',  # Замените на ваше имя пользователя
#         'PASSWORD': 'cheef',  # Замените на ваш пароль
#         # 'HOST': '10.159.8.163',  # Или другой хост, если необходимо
#         # 'HOST': 'localhost',  # Или другой хост, если необходимо
#         'HOST': '127.0.0.1',  # Или другой хост, если необходимо
#         'PORT': '3306',  # Порт по умолчанию для PostgreSQL
#     }
# ----------------------------postgresql
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',  # Замените на ваше имя пользователя
        'PASSWORD': 'postgres_oa',  # Замените на ваш пароль
        'HOST': '10.159.8.163',  # Или другой хост, если необходимо
        # 'HOST': 'localhost',  # Или другой хост, если необходимо
        # 'HOST': '127.0.0.1',  # Или другой хост, если необходимо
        'PORT': '5432',  # Порт по умолчанию для PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,  # Установите минимальную длину пароля на 4 символа
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'
DATE_FORMAT = 'Y m d'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# STATIC_URL = 'my_app_smp/static/'
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'my_app_smp/static'),
    os.path.join(BASE_DIR, 'my_app_smp',  'static'),
]

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / '/staticfiles'  # Путь к папке, куда будут собираться статические файлы

STATIC_URL = '/static/'
# STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'my_app_smp', 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'  # Замените 'home' на имя вашего представления
LOGOUT_REDIRECT_URL = 'login'  # Замените 'login' на имя вашего представления
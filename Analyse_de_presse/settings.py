"""
Django settings for Analyse_de_presse project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1gj%kxxxyk7^e$t@h@-=^an3u9gn1)f*8*)^c(rs4*!l1c=d4n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    'alimabrouk.pythonanywhere.com',
    'www.alimabrouk.pythonanywhere.com',
    '127.0.0.1',
    'localhost'
]





# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'AppScraping',  # Assurez-vous que votre application est listée ici
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    
    
]




ROOT_URLCONF = 'Analyse_de_presse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'App_Analyse_presse', 'Template')],
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

WSGI_APPLICATION = 'Analyse_de_presse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Analyse_presse',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3307',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',  # Or 'STRICT_ALL_TABLES' for more restrictions
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

DEBUG = True

USE_I18N = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#STATIC_URL = 'static/'
import os

# URL utilisée pour accéder aux fichiers statiques
STATIC_URL = '/static/'

# Définir les répertoires contenant les fichiers statiques (CSS, JS, images, etc.)
# Si vous utilisez le chemin absolu sous Windows, c'est ce format
STATICFILES_DIRS = [
    r'C:\Analyse_de_presse\AppScraping\static',  # Utilisation du chemin absolu pour Windows
]

# Répertoire où les fichiers statiques collectés seront stockés pour la production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

#setti,g authentification 
LOGIN_URL='/login/'
LOGIN_REDIRECT_URL=''

LOGOUT_URL='/logout/'
LOGOUT_REDIRECT_URL='/login/'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

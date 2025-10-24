"""
Django settings for config project.
"""

from decouple import config 
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY') 

DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'users', 
    'anymail', 
    'clientes.apps.ClientesConfig',
]

SITE_ID = 1 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.MinhaPasswordChangeMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'pt-br' 
TIME_ZONE = 'America/Sao_Paulo' 
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),] 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- MUDANÇA AQUI ---
# Configurações de Sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Desloga o usuário ao fechar o navegador
# --- FIM DA MUDANÇA ---


# Configurações de Login
LOGIN_URL = '/contas/login/'        
LOGIN_REDIRECT_URL = '/admin/'      

# Email Configs
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend') 
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='') 

ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default=""),
}
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='seu-email-aqui@dominio.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
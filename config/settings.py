# config/settings.py

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
        'core.apps.CoreConfig', # [ADICIONADO] Nosso novo app de configurações
        'js_asset',
        'widget_tweaks',
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
                                'core.context_processors.site_config_processor', 
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

# --- Configuração de Mídia (Uploads) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# --- FIM DA ADIÇÃO ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de Sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE = True 

# Configurações de Login
LOGIN_URL = '/login/' # Tela de login principal

# --- CORREÇÃO APLICADA AQUI ---
LOGIN_REDIRECT_URL = '/' 
# --- FIM DA CORREÇÃO ---


# ====================================================================
# [MODIFICADO] CONFIGURAÇÃO DINÂMICA DE E-MAIL
# As credenciais são lidas da tabela SiteConfiguracao (Admin)
# ====================================================================

# O Anymail é o backend que vamos usar se as credenciais ADMIN forem preenchidas.
# Se as credenciais no Admin estiverem vazias, o 'default' (console) será usado.
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend') 

# As configurações de host/porta/senha/tls SÃO IGNORADAS AQUI e lidas pela view.

# Se você estiver usando Anymail e precisar de uma chave GLOBAL (não dinâmica),
# ela fica aqui (mas não a usamos na view).
ANYMAIL = {
        "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default=""),
}

# Este é o e-mail remetente padrão de fallback (Será sobrescrito pelo Admin/SiteConfiguracao)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='seu-email-aqui@dominio.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ReCAPTCHA (ainda não usado, mas configurado)
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
NOCAPTCHA = True
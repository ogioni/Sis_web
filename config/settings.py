"""
Django settings for config project.
"""

# IMPORTANTE: Agora lemos as variáveis de ambiente com segurança
from decouple import config 
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# WARNING: LÊ DO ARQUIVO .env para segurança (não exponha no GitHub!)
# USE A SUA CHAVE ORIGINAL DENTRO DO ARQUIVO .env
SECRET_KEY = config('SECRET_KEY') 


# SECURITY WARNING: don't run with debug turned on in production!
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
    'clientes', # Novo: Para integração segura de E-mail (SendGrid, Mailgun, etc.)
]

# ID do Site (para montar links de e-mail)
SITE_ID = 1 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Nosso Vigia que Força a Troca de Senha
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
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br' 

TIME_ZONE = 'America/Sao_Paulo' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),] 


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configurações de Login
# Onde o Django deve buscar a tela de login
LOGIN_URL = '/contas/login/'        
# Para onde ir depois de logar com sucesso
LOGIN_REDIRECT_URL = '/admin/'


# =======================================================
# CONFIGURAÇÃO DE E-MAIL (PRODUÇÃO E TESTE)
# =======================================================

# Lê o EMAIL_BACKEND do .env. Se não encontrar (ou se você quiser teste), usa o console.
# Em produção, o .env terá: EMAIL_BACKEND=anymail.backends.sendgrid.EmailBackend
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend') 

# Credenciais de e-mail (lidas do .env)
# EMAIL_HOST_USER e SENDGRID_API_KEY devem ser configurados no seu arquivo .env
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Configurações do Anymail (para SendGrid)
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default=""),
}
DEFAULT_FROM_EMAIL = 'seu-email-aqui@dominio.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL # Usado para mensagens de erro do sistema

#Teste de Backup
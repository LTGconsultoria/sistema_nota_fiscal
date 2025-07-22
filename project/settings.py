from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^0e#i4u2re+yu&3#x@k1bxxd@ezkpu48q!ggvljtp=xh5aq9f!'

DEBUG = True

ALLOWED_HOSTS = [
    'ltgconsultoriadeinformatica.cloud',
    'www.ltgconsultoriadeinformatica.cloud',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Ajuste o código do idioma para 'pt-br'
LANGUAGE_CODE = 'pt-br'

# Ajuste o fuso horário para 'America/Sao_Paulo'
TIME_ZONE = 'America/Sao_Paulo'

# Certifique-se de que a internacionalização está ativada
USE_I18N = True

# Certifique-se de que a localização está ativada
USE_L10N = True

# Use o fuso horário especificado nas operações de tempo
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = '/login/'

# Segurança CSRF/HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://ltgconsultoriadeinformatica.cloud',
    'https://www.ltgconsultoriadeinformatica.cloud',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_USE_SESSIONS = False

# Importante: configura Django para confiar no HTTPS vindo do Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Evitar definir CSRF_COOKIE_DOMAIN manualmente a menos que necessário
# CSRF_COOKIE_DOMAIN = 'ltgconsultoriadeinformatica.cloud'
# SESSION_COOKIE_DOMAIN = 'ltgconsultoriadeinformatica.cloud'

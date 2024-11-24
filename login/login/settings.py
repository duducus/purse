from pathlib import Path
import os
from django.conf import settings
from django.conf.urls.static import static

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar configuración del entorno local si existe
try:
    from .settings_local import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9rc-4cwh0h3mvufrf9%myh7xp293to&$(jua7b^!neuj8ku$3e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','74.208.60.39','www.localgamestore.store']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'intercambios',
    'ventas',
    'torneos',
    'blog'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Cambia el nivel de Django a WARNING para evitar mensajes excesivos
            'propagate': True,
        },
        'core': {  # El nombre de tu app, asegúrate de que coincida con el nombre de tu módulo
            'handlers': ['console'],
            'level': 'DEBUG',  # Aquí mantienes el nivel de logging en DEBUG solo para tu código
            'propagate': True,
        },
        'intercambios': {  # El nombre de tu app, asegúrate de que coincida con el nombre de tu módulo
            'handlers': ['console'],
            'level': 'DEBUG',  # Aquí mantienes el nivel de logging en DEBUG solo para tu código
            'propagate': True,
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'login.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'core' / 'templates',
        ],
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

WSGI_APPLICATION = 'login.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_dev.sqlite3',
        #'NAME': BASE_DIR / 'db_prod.sqlite3',
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

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'  # Hora de México (Ciudad de México)
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

urlpatterns = [
    # ... tus otras rutas aquí
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'templates', 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

AUTH_USER_MODEL = 'core.CustomUser'

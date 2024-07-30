from pathlib import Path
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9rc-4cwh0h3mvufrf9%myh7xp293to&$(jua7b^!neuj8ku$3e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','74.208.60.39']
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de base de datos local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

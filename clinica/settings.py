"""
Configuración del proyecto Clínica Dental (Django 6.1).

Los datos sensibles (clave secreta y credenciales de PostgreSQL) se leen
del archivo .env, que NO se sube a GitHub, usando python-dotenv.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Carga las variables del archivo .env como variables de entorno.
# Debe ejecutarse antes de usar os.getenv().
load_dotenv()

# Carpeta raíz del proyecto (la que contiene manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Seguridad
# ---------------------------------------------------------------------------

# Clave secreta de Django, definida en el archivo .env.
SECRET_KEY = os.getenv('SECRET_KEY')

# En desarrollo debe ser True. En producción debe cambiarse a False.
DEBUG = True

# Dominios permitidos. En producción hay que indicar el dominio real.
ALLOWED_HOSTS = []


# ---------------------------------------------------------------------------
# Aplicaciones
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'citas',  # Nuestra app: pacientes, odontólogos, consultorios y citas.
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

ROOT_URLCONF = 'clinica.urls'

# Plantillas HTML. Con APP_DIRS=True, Django busca las plantillas dentro de
# la carpeta "templates" de cada app (por ejemplo, citas/templates/).
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

WSGI_APPLICATION = 'clinica.wsgi.application'


# ---------------------------------------------------------------------------
# Base de datos (PostgreSQL)
# ---------------------------------------------------------------------------
# Los valores se toman del archivo .env para no exponer la contraseña.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# ---------------------------------------------------------------------------
# Validación de contraseñas
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# Idioma y zona horaria
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Archivos estáticos (CSS, JavaScript, imágenes)
# ---------------------------------------------------------------------------

STATIC_URL = 'static/'


# ---------------------------------------------------------------------------
# Correo (en desarrollo, los correos se muestran en la consola)
# ---------------------------------------------------------------------------

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

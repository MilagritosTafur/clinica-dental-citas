"""
Configuración del proyecto Clínica Dental (Django 6.1).

Los datos sensibles (clave secreta y credenciales de PostgreSQL) se leen
del archivo .env, que NO se sube a GitHub, usando python-dotenv.
"""

import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from dotenv import load_dotenv

# Carpeta raíz del proyecto (la que contiene manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga los secretos de la app desde .env y las variables que Neon escribe
# con `neon deploy` desde .env.local. Debe ejecutarse antes de os.getenv().
# .env va primero para que sus valores tengan prioridad.
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR / '.env.local')


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
# Base de datos (PostgreSQL en Neon)
# ---------------------------------------------------------------------------
# `neon deploy` escribe en .env.local:
#   DATABASE_URL          -> endpoint pooled (con -pooler), para la app.
#   DATABASE_URL_UNPOOLED -> endpoint directo, para migraciones/pg_dump.
# La app usa la pooled por defecto. Para migrar, exporta
# DATABASE_URL="$DATABASE_URL_UNPOOLED" antes de `manage.py migrate`.

def _database_from_url(url):
    """Convierte una URL de conexión de Postgres (Neon) al dict de Django."""

    parts = urlparse(url)
    query = parse_qs(parts.query)

    # Opciones que Neon incluye en la URL y que Django pasa al driver.
    options = {
        clave: valores[0]
        for clave, valores in query.items()
        if clave in ('sslmode', 'channel_binding', 'options')
    }

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote(parts.path.lstrip('/')),
        'USER': unquote(parts.username or ''),
        'PASSWORD': unquote(parts.password or ''),
        'HOST': parts.hostname or '',
        'PORT': str(parts.port or ''),
        'OPTIONS': options,
    }


DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {'default': _database_from_url(DATABASE_URL)}
else:
    # Reserva: credenciales sueltas, por si no hay DATABASE_URL.
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

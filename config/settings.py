from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
# En Vercel exigimos una clave real; localmente mantenemos la clave didáctica.
ON_VERCEL = bool(os.getenv('VERCEL'))
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if ON_VERCEL and not SECRET_KEY:
    raise RuntimeError('Falta DJANGO_SECRET_KEY en las variables de entorno de Vercel')
SECRET_KEY = SECRET_KEY or 'clave-local-solo-para-la-clase-cambiar-en-produccion'
DEBUG = os.getenv('DJANGO_DEBUG', 'False' if ON_VERCEL else 'True').lower() == 'true'
if ON_VERCEL:
    DEBUG = False  # Nunca mostrar trazas ni configuraciones privadas en Vercel.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']
# Django necesita reconocer el dominio HTTPS en formularios POST desde Vercel.
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
# Vercel termina HTTPS delante de Django.
if ON_VERCEL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'estudiantes',
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
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'

# CLASE: usar SQLite por defecto; al editar .env a supabase, Django usa PostgreSQL.
if os.getenv('DB_ENGINE', 'sqlite').lower() == 'supabase':
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': 10,
            # Transaction pooler de Supabase (6543) no admite prepared statements.
            # Session pooler local (5432) también funciona con esta opción.
            'prepare_threshold': None,
        },
        'CONN_MAX_AGE': 0,
    }}
else:
    if ON_VERCEL:
        raise RuntimeError('En Vercel configura DB_ENGINE=supabase; SQLite no es persistente')
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}

AUTH_PASSWORD_VALIDATORS = []  # Proyecto demostrativo sin autenticación de usuarios
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

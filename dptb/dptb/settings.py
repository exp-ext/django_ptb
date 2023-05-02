"""
Django settings for dptb project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import socket
from pathlib import Path, PurePath

from core.keygen import get_key
from dotenv import load_dotenv

load_dotenv()

# bots settings
DOMAIN_NAME = os.getenv('DOMAIN_NAME')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
YANDEX_GEO_API_TOKEN = os.getenv('YANDEX_GEO_API_TOKEN', default='some_token_to_pass_test')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    SECRET_KEY = get_key(50)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost'
).split(' ')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # celery
    'django_celery_beat',
    # debugger
    'debug_toolbar',
    # my app
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'tgbot.apps.TelbotConfig',
]

MIDDLEWARE = [
    # django
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Authentication
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # debug_toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'dptb.urls'
TEMPLATES_DIR = os.fspath(PurePath(BASE_DIR, 'templates'))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'dptb.wsgi.application'
ASGI_APPLICATION = 'dptb.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TIME_ZONE': 'UTC',
    }
}

POSTGRES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

DATABASES = SQLITE if DEBUG else POSTGRES

# django-dbbackup
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location': os.fspath(PurePath(BASE_DIR, 'backup')),
}

DBBACKUP_CONNECTORS = {
    'default': {
        'CONNECTOR': 'dbbackup.db.postgresql.PgDumpBinaryConnector',
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation and security
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'index'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Для корректной работы виджета в форме профиля
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

STATIC_DIR = os.fspath(PurePath(BASE_DIR, 'static'))

if DEBUG:
    STATICFILES_DIRS = (STATIC_DIR,)
else:
    STATIC_ROOT = STATIC_DIR

# MEDIA
MEDIA_URL = '/media/'

MEDIA_ROOT = os.fspath(PurePath(BASE_DIR, 'media'))

# Setting for working with Jupiter
if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = ([ip[: ip.rfind(".")] + ".1" for ip in ips]
                    + ["127.0.0.1", "10.0.2.2"])

# Celery
if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_IGNORE_RESULT = True


# REDIS
# https://python-scripts.com/redis
# https://redis.io/docs/
# CELERY
# https://django.fun/ru/docs/celery/5.1/getting-started/introduction/
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'

# CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CACHE BACKEND
REDISCACHE = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_URL}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

LOCMEMCACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHES = LOCMEMCACHE if DEBUG else REDISCACHE

# USER AGENTS PARSING
# Cache backend is optional, but recommended to speed up user agent parsing
# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
# https://pypi.org/project/django-user-agents/
USER_AGENTS_CACHE = 'default'

import os

import yaml
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'settings/config.yaml')) as f:
    config = yaml.load(f.read())

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'somsolet.apps.SomsoletConfig',
    'crispy_forms',
    'django_tables2',
    'django_filters',
    'import_export',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'django_rq',
    'anymail',
    'django_extensions',
    'widget_tweaks',
    'django',
    'jquery',
    'rosetta',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            './somsolet/templates',
            './somsolet/static/html'
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

WSGI_APPLICATION = 'config.wsgi.application'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = 'bootstrap4-som.html'
IMPORT_EXPORT_USE_TRANSACTIONS = True
BOOTSTRAP4 = {
    'include_jquery': True,
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/somsolet/profile_engineering/'
LOGOUT_REDIRECT_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
    ('ca', _('Catalan')),
    ('es', _('Spanish')),
    ('eu', _('Basque')),
    ('gl', _('Galician')),
)

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join((BASE_DIR), '../locale'),
]


# Rosetta conf
ROSETTA_ENABLE_REFLANG = True
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_LOGIN_URL = '/admin'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
MEDIA_URL = '/uploaded_files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded_files')
FILE_UPLOAD_PERMISSIONS = 0o644

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATA_UPLOAD_MAX_NUMBER_FIELDS=None

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}
RQ_SHOW_ADMIN_LINK = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            'class': 'logging.StreamHandler',
            "formatter": "simple",
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': 'log/somsolet.log',
            'when': 'midnight',
            'backupCount': 7
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'somsolet': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        "scheduler_tasks": {
            "handlers": ["console", "file"],
            "level": "DEBUG"
        },
    }
}


ANYMAIL = {
    'SENDGRID_API_KEY': config['sendgrid_api_key'],
    'EMAIL_HOST': 'smtp.sendgrid.net',
    'EMAIL_HOST_USER': 'apikey',
    'EMAIL_HOST_PASSWORD': config['sendgrid_api_key'],
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = [config['email']['default_from']]
BCC = [config['email']['bcc']]

import os
import sentry_sdk
import yaml

from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .. import VERSION

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, "config/settings/config.yaml")) as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "somsolet.apps.SomsoletConfig",
    "admin_auto_filters",
    "crispy_forms",
    "crispy_bootstrap4",
    "django_tables2",
    "django_filters",
    "import_export",
    "bootstrap4",
    "bootstrap_datepicker_plus",
    "django_rq",
    "anymail",
    "django_extensions",
    "widget_tweaks",
    "django",
    "jquery",
    "rosetta",
    "hijack",
    "hijack.contrib.admin",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hijack.middleware.HijackUserMiddleware",
]


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["./somsolet/templates", "./static/html"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
DJANGO_TABLES2_TEMPLATE = "bootstrap4-som.html"
IMPORT_EXPORT_USE_TRANSACTIONS = True
BOOTSTRAP4 = {
    "include_jquery": True,
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_REDIRECT_URL = "/somsolet/profile_engineering/"
LOGOUT_REDIRECT_URL = "login"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGE_CODE_EN = "en"
LANGUAGE_CODE_CA = "ca"
LANGUAGE_CODE_ES = "es"
LANGUAGE_CODE_EU = "eu"
LANGUAGE_CODE_GL = "gl"

LANGUAGES = (
    (LANGUAGE_CODE_EN, _("English")),
    (LANGUAGE_CODE_CA, _("Catalan")),
    (LANGUAGE_CODE_ES, _("Spanish")),
    (LANGUAGE_CODE_EU, _("Basque")),
    (LANGUAGE_CODE_GL, _("Galician")),
)

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# Rosetta conf
ROSETTA_ENABLE_REFLANG = True
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_LOGIN_URL = "/admin"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
MEDIA_URL = "/uploaded_files/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded_files")
FILE_UPLOAD_PERMISSIONS = 0o644

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "DEFAULT_TIMEOUT": 360,
    },
    "low": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
    },
    "email": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 1,
    },
}
RQ_SHOW_ADMIN_LINK = True
RQ_JOB_DEFAULT_TIMEOUT = 180

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "simple",
            "filename": "log/somsolet.log",
            "when": "midnight",
            "backupCount": 7,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "somsolet": {"handlers": ["console"], "level": "INFO"},
        "scheduler_tasks": {"handlers": ["console", "file"], "level": "DEBUG"},
    },
}


ANYMAIL = {
    "SENDGRID_API_KEY": config["sendgrid_api_key"],
    "EMAIL_HOST": "smtp.sendgrid.net",
    "EMAIL_HOST_USER": "apikey",
    "EMAIL_HOST_PASSWORD": config["sendgrid_api_key"],
    "EMAIL_PORT": 587,
    "EMAIL_USE_TLS": True,
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = [config["email"]["default_from"]]
BCC = [config["email"]["bcc"]]


# Sentry
SENTRY_DSN = config["sentry_dsn"]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=os.environ["DJANGO_SETTINGS_MODULE"].split(".")[-1],
    release=VERSION,
)

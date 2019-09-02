import os
import yaml


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'settings/config.yaml')) as f:
    config = yaml.load(f.read())


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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./somsolet/templates', ],
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
DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4-som.html'
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
MEDIA_URL = '/home/usuario/Documentos/somenergia-solarprosumers/solarprosumers/somsolet/uploaded_files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded_files')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


from .base import *
import yaml

with open(os.path.join(BASE_DIR, 'settings/config.yaml')) as f:
    config = yaml.load(f.read())

SECRET_KEY = config['secret_key']

ALLOWED_HOSTS = [
    'somsolet.somenergia.coop'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['databases']['name'],
        'USER': config['databases']['user'],
        'PASSWORD': config['databases']['password'],
        'HOST': config['databases']['host'],
        'PORT': config['databases']['port'],
    },
    'mongodb': {
        'HOST': config['mongodb']['host'],
        'PORT': config['mongodb']['port'],
        'USER': config['mongodb']['user'],
        'PASSWORD': config['mongodb']['password'],
        'NAME': config['mongodb']['name']
    }
}

RQ_QUEUES = {
    'default': {
        'URL': config['redis']['url'],
    },
    'low': {
        'URL': config['redis']['url'],
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

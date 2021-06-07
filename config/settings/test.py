from .base import *

SECRET_KEY = config['secret_key']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['databases']['name'],
        'USER': config['databases']['user'],
        'PASSWORD': config['databases']['password'],
        'HOST': config['databases']['host'],
        'PORT': config['databases']['port'],
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

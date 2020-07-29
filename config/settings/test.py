from .base import *

SECRET_KEY = config['secret_key']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['databases']['test']['name'],
        'USER': config['databases']['test']['user'],
        'PASSWORD': config['databases']['test']['password'],
        'HOST': config['databases']['test']['host'],
        'PORT': config['databases']['test']['port'],
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

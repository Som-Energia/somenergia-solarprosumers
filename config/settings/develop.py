from .base import *
import yaml

with open(os.path.join(BASE_DIR, 'settings/config.yaml')) as f:
    config = yaml.load(f.read())

SECRET_KEY = 'e2#ihl8s%jy2r4s1do0*z4jin222o^w%%ddn-(nr=3n*bygch^'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['databases']['develop']['name'],
        'USER': config['databases']['develop']['user'],
        'PASSWORD': config['databases']['develop']['password'],
        'HOST': config['databases']['develop']['host'],
        'PORT': config['databases']['develop']['port'],
    },
    'mongodb': {
        'HOST': config['mongodb']['host'],
        'PORT': config['mongodb']['port'],
        'USER': config['mongodb']['user'],
        'PASSWORD': config['mongodb']['password'],
        'NAME': config['mongodb']['name']
    }
}
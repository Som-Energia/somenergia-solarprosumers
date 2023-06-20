import yaml

from .base import *

SECRET_KEY = "e2#ihl8s%jy2r4s1do0*z4jin222o^w%%ddn-(nr=3n*bygch^"

DEBUG = True

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["databases"]["name"],
        "USER": config["databases"]["user"],
        "PASSWORD": config["databases"]["password"],
        "HOST": config["databases"]["host"],
        "PORT": config["databases"]["port"],
    },
    "mongodb": {
        "HOST": config["mongodb"]["host"],
        "PORT": config["mongodb"]["port"],
        "USER": config["mongodb"]["user"],
        "PASSWORD": config["mongodb"]["password"],
        "NAME": config["mongodb"]["name"],
    },
}

INTERNAL_IPS = ["127.0.0.1"]

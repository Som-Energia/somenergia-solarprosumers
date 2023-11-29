from .base import *

SECRET_KEY = config["secret_key"]

ALLOWED_HOSTS = config["allowed_hosts"]

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

RQ_QUEUES = {
    "default": {
        "URL": config["redis"]["url"],
    },
    "low": {
        "URL": config["redis"]["url"],
    },
    "email": {"URL": config["redis"]["url"]},
}

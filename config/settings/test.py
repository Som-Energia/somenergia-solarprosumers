from .base import *
import yaml

with open(os.path.join(BASE_DIR, "settings/config.yaml")) as f:
    config = yaml.load(f.read())

SECRET_KEY = config["secret_key"]

ALLOWED_HOSTS = ["somsolet-demo.somenergia.local"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["databases"]["test"]["name"],
        "USER": config["databases"]["test"]["user"],
        "PASSWORD": config["databases"]["test"]["password"],
        "HOST": config["databases"]["test"]["host"],
        "PORT": config["databases"]["test"]["port"],
    }
}

RQ_QUEUES = {
    "default": {
        "URL": config["redis"]["url"],
    },
    "low": {
        "URL": config["redis"]["url"],
    },
}

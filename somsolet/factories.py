from typing import Any, Dict

from somsolet.models import Project
from somsolet.validators import SendRegistrationEmailValidator


class Factory(object):
    _instances: Dict[Any, Any] = {}

    @classmethod
    def instance(cls, id, create_instance):
        if id not in cls._instances:
            cls._instances[id] = create_instance()

        return cls._instances[id]


def send_registration_email_validator():
    return Factory.instance(
        "send_registration_email_validator",
        lambda: SendRegistrationEmailValidator(project_model=Project),
    )

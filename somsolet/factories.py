from typing import Any, Dict

from somsolet.services import EmailService
from somsolet.tasks import SendRegistrationTask


class Factory(object):
    _instances: Dict[Any, Any] = {}

    @classmethod
    def instance(cls, id, create_instance):
        if id not in cls._instances:
            cls._instances[id] = create_instance()
        return cls._instances[id]


def email_service():
    return Factory.instance("email_service", lambda: EmailService())


def send_registration_task():
    return Factory.instance(
        "send_registration_task",
        lambda: SendRegistrationTask(email_service()),
    )

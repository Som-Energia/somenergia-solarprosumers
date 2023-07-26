from typing import Any, Dict, Callable

from somsolet.services import EmailService, EmailNotification


class Factory(object):
    _instances: Dict[Any, Any] = {}

    @classmethod
    def instance(cls, id_: str, create_instance: Callable):
        if id_ not in cls._instances:
            cls._instances[id_] = create_instance()
        return cls._instances[id_]


def email_service() -> EmailService:
    return Factory.instance("email_service", lambda: EmailService())


def email_notification() -> EmailNotification:
    return Factory.instance(
        "email_notification",
        lambda: EmailNotification(email_service()),
    )

import logging

from django.conf import settings
from django_rq import job

from .factories import email_notification
from .models import Project

logger = logging.getLogger("rq.worker")


@job("email", timeout=settings.RQ_JOB_DEFAULT_TIMEOUT)
def send_registration_email(project: Project) -> None:
    email_notification().send_registration_email(project)

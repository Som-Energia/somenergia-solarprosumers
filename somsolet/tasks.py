import logging

from django.conf import settings
from django.utils import timezone
from django.utils.translation import override, gettext_lazy as _
from django_rq import job

from scheduler_tasks import send_email

from .models import ClientFile

logger = logging.getLogger("rq.worker")


class SendRegistrationTask:
    def __init__(self, email_service):
        self.email_service = email_service

    @job(settings.RQ_QUEUES["email"], timeout=settings.RQ_JOB_DEFAULT_TIMEOUT)
    def send_registration_email(self, project):
        if project.registration_email_is_sent:
            logger.info(
                "Registration email has already been sent to: %s", project.client.name
            )
            return

        lang = project.client.language

        general_conditions = ClientFile.objects.get(
            name="General Conditions", language=lang
        )
        with override(lang):
            message_params = {
                "header": _("Hola {},").format(project.client.name),
                "ending": _("Salut i bona energia,"),
            }

            self.email_service.send_email(
                to_email=[project.client.email],
                subject=_(
                    "Confirmació d'Inscripció a la Compra Col·lectiva Som Energia"
                ),
                message_params=message_params,
                email_template="emails/message_body_general_conditions.html",
                filename=general_conditions.file.path,
            )

        project.registration_email_sent = True
        project.registration_email_sent_date = timezone.now()
        project.save()
        logger.info("Registration email has been sent to: %s", project.client.name)

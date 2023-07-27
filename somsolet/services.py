import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override
from django.db.transaction import atomic

from .models import ClientFile, Project

logger = logging.getLogger("rq.worker")


class EmailService:
    def send_email(
        self,
        to_email: list,
        subject: str,
        message_params: dict,
        email_template: str,
        filename: str = "",
        from_email: str = "",
    ) -> None:
        html_body = render_to_string(email_template, message_params)
        msg = EmailMessage(
            subject,
            html_body,
            from_email,
            to_email,
            settings.BCC,
        )
        if filename:
            msg.attach_file(filename)
        msg.content_subtype = "html"
        msg.send()


class EmailNotification:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def send_registration_email(self, project: Project) -> None:
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

        with atomic():
            project.registration_email_sent = True
            project.registration_email_sent_date = timezone.now()

            if not project.client.sent_general_conditions:
                project.client.sent_general_conditions = True
                project.client.sent_general_conditions_date = timezone.now()
                project.client.save()
            project.save()

        logger.info("Registration email has been sent to: %s", project.client.name)

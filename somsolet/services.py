from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.settings.base import BCC


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
            BCC,
        )
        if filename:
            msg.attach_file(filename)
        msg.content_subtype = "html"
        msg.send()

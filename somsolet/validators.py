from somsolet.models import Project


class SendRegistrationEmailValidator:
    def registration_email_is_sent(self, project: Project) -> bool:
        if project.registration_email_sent:
            return True
        return False

from somsolet.models import Project


class SendRegistrationEmailValidator:
    def __init__(self, project_model: Project):
        self.Project = project_model

    def registration_email_is_sent(self, project: Project) -> bool:
        if project.registration_email_sent:
            return True
        return False

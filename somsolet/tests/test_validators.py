from django.test import TestCase

from somsolet.models import Project
from somsolet.validators import SendRegistrationEmailValidator


class TestSendRegistrationEmailValidator(TestCase):
    def test__registration_email_is_sent(self):
        # having a project with registration_email_sent=False
        project = Project.objects.create(
            name="test",
            campaign=None,
            client=None,
            registration_email_sent=False,
        )
        sut = SendRegistrationEmailValidator(project_model=Project)

        # if registration email has not been sent
        result = sut.registration_email_is_sent(project)

        # it returns False
        assert result is False

    def test__registration_email_is_not_sent(self):
        # having a project with registration_email_sent=True
        project = Project.objects.create(
            name="test",
            campaign=None,
            client=None,
            registration_email_sent=True,
        )
        sut = SendRegistrationEmailValidator(project_model=Project)

        # if registration email has been sent
        result = sut.registration_email_is_sent(project)

        # it returns True
        assert result is True

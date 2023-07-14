from django.test import TestCase

from somsolet.models import Project


class TestProject(TestCase):
    def test__project__registration_email_is_sent(self):
        # having a project with registration_email_sent=False
        project = Project.objects.create(
            name="test",
            campaign=None,
            client=None,
            registration_email_sent=False,
        )

        # if registration email has not been sent
        result = project.registration_email_is_sent

        # it returns False
        assert result is False

    def test__project__registration_email_is_not_sent(self):
        # having a project with registration_email_sent=True
        project = Project.objects.create(
            name="test",
            campaign=None,
            client=None,
            registration_email_sent=True,
        )

        # if registration email has been sent
        result = project.registration_email_is_sent

        # it returns True
        assert result is True

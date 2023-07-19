import pytest

from unittest import TestCase
from expects import expect
from doublex import Spy, when
from doublex_expects import have_been_called_with, have_been_called

from somsolet.services import EmailService
from somsolet.tasks import SendRegistrationTask
from somsolet.tests.factories import ProjectFactory, ClientFactory


class TestTask(TestCase):
    @pytest.mark.django_db
    def test__send_registration_email__already_sent(self):
        project = ProjectFactory(registration_email_sent=True, client=ClientFactory())
        email_service = Spy(EmailService)
        sut = SendRegistrationTask(email_service)

        sut.send_registration_email(project=project)

        expect(email_service.send_email).not_to(have_been_called)

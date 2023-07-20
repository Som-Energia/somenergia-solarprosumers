import pytest

from unittest import TestCase
from mock import patch
from expects import expect, match
from doublex import Spy
from doublex_expects import have_been_called_with, have_been_called
from django.utils import timezone

import datetime

from somsolet.models import Project
from somsolet.services import EmailService
from somsolet.tasks import SendRegistrationTask
from somsolet.tests.factories import ProjectFactory, ClientFactory


class TestTask(TestCase):
    @pytest.mark.django_db
    def test__send_registration_email(self):
        project = ProjectFactory(registration_email_sent=False, client=ClientFactory())
        email_service = Spy(EmailService)
        sut = SendRegistrationTask(email_service)

        with patch.object(
            timezone,
            "now",
            return_value=datetime.datetime(2015, 1, 8, 11, 00, tzinfo=timezone.utc),
        ) as mock_now:
            sut.send_registration_email(project=project)

            expect(email_service.send_email).to(
                have_been_called_with(
                    to_email=[project.client.email],
                    subject="Confirmació d'Inscripció a la Compra Col·lectiva Som Energia",
                    message_params={
                        "header": f"Hola {project.client.name},",
                        "ending": f"Salut i bona energia,",
                    },
                    email_template="emails/message_body_general_conditions.html",
                    filename=match(
                        "^.*Condicions_Generals_de_les_Compres_Col_lectives_de_(.*).pdf"
                    ),
                )
            )
            last_saved_project = Project.objects.latest("id")
            assert last_saved_project.registration_email_sent is True
            assert (
                last_saved_project.registration_email_sent_date == mock_now.return_value
            )

    @pytest.mark.django_db
    def test__send_registration_email__already_sent(self):
        project = ProjectFactory(registration_email_sent=True, client=ClientFactory())
        email_service = Spy(EmailService)
        sut = SendRegistrationTask(email_service)

        sut.send_registration_email(project=project)

        expect(email_service.send_email).not_to(have_been_called)

import tempfile

import pytest

from somsolet.services import EmailService

from config.settings.base import DEFAULT_FROM_EMAIL


@pytest.fixture
def from_email():
    return DEFAULT_FROM_EMAIL


@pytest.fixture
def attachment():
    attachment = tempfile.NamedTemporaryFile()
    yield attachment.name
    attachment.close()


@pytest.fixture
def email_template():
    return "test_email_service.html"


@pytest.fixture
def email_data(email_template, attachment):
    return dict(
        to_email="test@email",
        subject="test_subject",
        message_params=dict(
            foo="foo",
            bar="bar",
        ),
        email_template=email_template,
        filename=attachment,
    )


class TestEmailService:
    def test__send_email__with_attachment(
        self, settings, email_data, from_email, attachment, mailoutbox
    ):
        settings.TEMPLATES = [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": ["./somsolet/tests/templates/"],
            },
        ]

        email_service = EmailService()

        email_service.send_email(
            [email_data["to_email"]],
            email_data["subject"],
            email_data["message_params"],
            email_data["email_template"],
            email_data["filename"],
            from_email,
        )

        m = mailoutbox[0]
        assert m.subject == "test_subject"
        assert (
            m.body
            == "foo Pecador papaar papaar a gramenawer de la pradera ese que llega te voy a borrar el cerito a peich bar\n"
        )
        assert m.from_email == from_email
        assert len(m.attachments) >= 1
        assert list(m.to) == ["test@email"]

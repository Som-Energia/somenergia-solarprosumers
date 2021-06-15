
import pytest
from django.core import mail
from django.utils.translation import gettext_lazy as _

from somsolet.tests.fixtures import *
import scheduler_tasks

@pytest.mark.django_db
class TestMailing:

    @pytest.mark.usefixtures('mailing_signature', 'campaign__solar_paco')
    def test_send_pending_notification__base_case(
         self, mailing_signature
    ):

        scheduler_tasks.send_pending_notification()
        email_template = 'emails/signature.html'

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.subject == _(f'CONTRACTE CLAU EN MÀ [Instalació plaques Montserrat Escayola] - Solar Paco, compra col·lectiva de Som Energia')
        assert 'Per qualsevol consulta pots respondre' in email.body
        #to do: add client language to test translations
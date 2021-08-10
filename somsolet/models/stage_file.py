import os

from config.settings import base
from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseFile(models.Model):

    date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date File'),
    )

    check = models.BooleanField(
        default=False,
        verbose_name=_('Checked?')
    )

    def update_upload(self, upload):
        self.upload = upload
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.save()

    def set_check(self, check):
        self.check = check
        self.save()

    def get_status(self):
        if self.date:
            return self.next_status
        else:
            return self.current_status

    class Meta:
        abstract = True


class SignatureFile(BaseFile):

    next_status = 'signature'
    current_status = 'offer'
    template = 'emails/signature.html'

    upload = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        return {
            'subject': _(f'CONTRACTE CLAU EN MÀ [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': str(os.path.join(base.MEDIA_ROOT, str(noti.project.signature.upload))),
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class PermitFile(BaseFile):

    next_status = 'construction permit'
    current_status = 'signature'
    template = ''

    upload = models.FileField(
        upload_to='uploaded_files/permit',
        default='uploaded_files/permit/som.png',
        verbose_name=_('Upload File')
    )


class OfferFile(BaseFile):

    next_status = 'offer'
    current_status = 'report'
    template = 'emails/offer.html'

    upload = models.FileField(
        upload_to='uploaded_files/offer',
        default='uploaded_files/offer/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        return {
            'subject': _(f'OFERTA ACCEPTADA [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': str(os.path.join(base.MEDIA_ROOT, str(noti.project.signature.upload))),
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }
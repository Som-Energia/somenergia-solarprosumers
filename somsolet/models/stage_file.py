from config.settings import base
from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime

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

    def set_is_invalid(self, is_invalid):
        self.is_invalid = is_invalid
        self.save()

    def get_status(self):
        if self.is_invalid:
            return self.current_status
        else:
            return self.next_status


    class Meta:
        abstract = True


class SignatureFile(BaseFile):

    next_status = 'signature'
    current_status = 'offer'
    template = ''

    upload = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        return {
            _(f'CONTRACTE CLAU EN MÀ [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            self.template,
            message_params,
            str(os.path.join(base.MEDIA_ROOT, str(noti.project.signature.upload))),
            message_params['email']
        }
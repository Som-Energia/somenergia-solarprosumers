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
    template = ''

    upload = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload File')
    )

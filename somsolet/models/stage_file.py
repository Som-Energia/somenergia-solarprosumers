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
        if self.date and not self.check:
            return self.next_status
        if self.check:
            return self.review_status
        else:
            return self.current_status

    class Meta:
        abstract = True


class PrereportStage(BaseFile):
    next_status = 'prereport'
    current_status = 'registered'
    review_status = 'prereport review'
    template = 'emails/prereport.html'

    upload = models.FileField(
        upload_to='uploaded_files/prereport',
        default='uploaded_files/prereport/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
            'campaign': noti.project.campaign,
            'address': [data['engineerings__address'] for data in campaign_data][0]
        }

        return {
            'subject': _(f'PREINFORME [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.prereport.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class ReportStage(BaseFile):
    next_status = 'report'
    current_status = 'prereport'
    review_status = 'report review'

    upload = models.FileField(
        upload_to='uploaded_files/report',
        default='uploaded_files/report/som.png',
        verbose_name=_('Upload File')
    )


class OfferStage(BaseFile):

    next_status = 'offer review'
    current_status = 'report'
    template = 'emails/offer.html'

    upload = models.FileField(
        upload_to='uploaded_files/offer',
        default='uploaded_files/offer/som.png',
        verbose_name=_('Upload File')
    )

    def get_status(self):
        if self.date:
            return self.next_status
        else:
            return self.current_status

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0]
        }

        return {
            'subject': _(f'INFORME TÈCNIC [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.report.upload))),
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.offer.upload)))
                ],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class OfferAcceptedStage(BaseFile):

    next_status = 'offer accepted'
    current_status = 'offer review'
    template = 'emails/offer_accepted.html'

    def get_status(self):
        if self.check:
            return self.next_status
        else:
            return self.current_status

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
            'attachment': [
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.offer_accepted.upload)))
                ],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class SignatureStage(BaseFile):

    next_status = 'signature'
    current_status = 'offer acepted'
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
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.signature.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class FirstInvoiceStage(BaseFile):
    next_status = 'first invoice'
    current_status = 'signature'
    template = 'emails/first_invoice.html'

    upload = models.FileField(
        upload_to='uploaded_files/first_invoice',
        default='uploaded_files/first_invoice/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
        }

        return {
            'subject': _(f'FACTURA 50% [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.first_invoice.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class PermitStage(BaseFile):

    next_status = 'construction permit'
    current_status = 'signature'
    template = 'emails/permit.html'

    upload = models.FileField(
        upload_to='uploaded_files/permit',
        default='uploaded_files/permit/som.png',
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
            'subject': _(f"TRAMITACIÓ LLICÈNCIA D'OBRES [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia"),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.permit.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class DeliveryCertificateStage(BaseFile):

    next_status = 'end installation'
    current_status = 'date installation set'

    upload = models.FileField(
        upload_to='uploaded_files/delivery_certificate',
        default='uploaded_files/delivery_certificate/som.png',
        verbose_name=_('Upload File')
    )


class SecondInvoiceStage(BaseFile):
    next_status = 'second invoice'
    current_status = 'end installation'
    template = 'emails/second_invoice.html'

    upload = models.FileField(
        upload_to='uploaded_files/second_invoice',
        default='uploaded_files/second_invoice/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
        }

        return {
            'subject': _(f'CONFIRMACIÓ DE PAGAMENT [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.second_invoice.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class LegalRegistrationStage(BaseFile):

    next_status = 'legal registration'
    current_status = 'end installation'
    template = 'emails/legal_registration.html'

    upload = models.FileField(
        upload_to='uploaded_files/legal_registration_docs',
        default='uploaded_files/legal_registration_docs/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
            'selfconsumption_modality': _('https://ca.support.somenergia.coop/article/801-que-he-de-fer-per-passar-el-meu-contracte-a-la-modalitat-amb-autoproduccio')
        }

        return {
            'subject': _(f'CERTIFICAT TRAMITACIÓ REGISTRE [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.legal_registration.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class LegalizationStage(BaseFile):
    next_status = 'legalization'
    current_status = 'legal registration'
    template = 'emails/legalization.html'

    rac_file = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/rac_file.png',
        verbose_name=_('Uploaded RAC File')
    )

    ritsic_file = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/ritsic_file.png',
        verbose_name=_('Uploaded RITSIC File')
    )

    cie_file = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/cie_file.png',
        verbose_name=_('Uploaded CIE File')
    )

    def update_rac(self, upload):
        self.rac_file = upload
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.save()

    def update_ritsic(self, upload):
        self.ritsic_file = upload
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.save()

    def update_cie(self, upload):
        self.cie_file = upload
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.save()

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
            'distributor_company': _('https://ca.support.somenergia.coop/article/655-les-distribuidores-d-electricitat')
        }

        return {
            'subject': _(f'CERTIFICAT LEGALITZACIÓ [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.rac_file.upload))),
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.ritsic_file.upload))),
                str(os.path.join(base.MEDIA_ROOT, str(noti.project.cie_file.upload))),
            ],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }


class LastInvoiceStage(BaseFile):
    next_status = 'last invoice'
    current_status = 'legalization'
    template = 'emails/last_invoice.html'

    upload = models.FileField(
        upload_to='uploaded_files/last_invoice',
        default='uploaded_files/last_invoice/som.png',
        verbose_name=_('Upload File')
    )

    def email_data(self, noti, campaign_data):
        message_params = {
            'header': _("Hola {},").format(noti.project.client.name),
            'ending': _("Salut i fins ben aviat!"),
            'engineering': [data['engineerings__name'] for data in campaign_data][0],
            'email': [data['engineerings__email'] for data in campaign_data][0],
        }

        return {
            'subject': _(f'CONFIRMACIÓ DE PAGAMENT [{noti.project}] - {noti.project.campaign}, compra col·lectiva de Som Energia'),
            'template': self.template,
            'message_params': message_params,
            'attachment': [str(os.path.join(base.MEDIA_ROOT, str(noti.project.last_invoice.upload)))],
            'from_email': base.DEFAULT_FROM_EMAIL[0]
        }
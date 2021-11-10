from datetime import datetime

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from .admin import Engineering
from .campaign import Campaign
from .choices_options import (BATERY_BRAND, INVERSOR_BRAND, ITEM_ANGLES,
                              ITEM_DISCARDED_TYPES, ITEM_ORIENTATION,
                              ITEM_STATUS, ITEM_WARNINGS, PANELS_BRAND,
                              PANELS_TYPE)
from .client import Client
from .stage_file import (SignatureStage, PermitStage, LegalRegistrationStage,
                         LegalizationStage, PrereportStage, OfferStage,
                         OfferAcceptedStage, SecondInvoiceStage, DeliveryCertificateStage,
                         ReportStage)

class ProjectQuerySet(models.QuerySet):

    def get_project(self, project_id, user):
        try:
            if user.is_superuser:
                return self.get(id=project_id)
            return self.get(
                id=project_id, engineering__user=user
            )
        except Project.DoesNotExist:
            return None


class Project(models.Model):

    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Installation'),
        help_text=_('Installation name')
    )

    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Campaign'),
        help_text=_('Campaign of this project')
    )

    engineering = models.ForeignKey(
        Engineering,
        null=True,
        blank=True,
        related_name='projects',
        on_delete=models.SET_NULL,
        verbose_name=_('Engineering'),
        help_text=_('Engineering responsable of this project')
    )

    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Client'),
        help_text=_('Client of this project')
    )

    status = models.CharField(
        choices=ITEM_STATUS,
        default=_('empty status'),
        max_length=50,
        verbose_name=_('State'),
        help_text=_('State of the project')
    )

    warning = models.CharField(
        choices=ITEM_WARNINGS,
        default=_('No Warn'),
        max_length=100,
        verbose_name=_('Warning'),
        help_text=_('Items to be aware')
    )

    warning_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Warning date'),
        help_text=_('Date when the warning raised')
    )

    preregistration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Preregistration Date'),
        help_text=_('Date of the project preregistration')
    )

    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('Paid Preregistration'),
        help_text=_('Check that indicates if preristration is paid')
    )

    registration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Registration date'),
        help_text=_('Date when de project was already registrated')
    )

    is_cch_downloaded = models.BooleanField(
        default=False,
        verbose_name=_('CCH downloaded'),
        help_text=_('Check that indicates if cch curves has been downloaded')
    )

    date_cch_download = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date CCH downloaded'),
        help_text=_('Date when cch curves were downloaded')
    )

# -------------------------- PrereprtStage -------------------------
    date_prereport = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date prereport'),
        help_text=_('Date when prereport was uploaded')
    )

    is_invalid_prereport = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Prereport?'),
        help_text=_('Check that indicates if prereport is incorrect or not')
    )

    upload_prereport = models.FileField(
        upload_to='uploaded_files/prereport',
        default='uploaded_files/prereport/som.png',
        verbose_name=_('Upload Prereport'),
        help_text=_('Prereport file')
    )

    prereport = models.ForeignKey(
        PrereportStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Prereport data')
    )
# -------------------------- Technical Visit-------------------------

    date_technical_visit = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date technical visit'),
    )
# -------------------------- ReportStage -------------------------

    report = models.ForeignKey(
        ReportStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Report data')
    )

    date_report = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date report'),
        help_text=_('Date when report was uploaded')
    )

    is_invalid_report = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Report?'),
        help_text=_('Check that indicates if report is incorrect or not')
    )

    upload_report = models.FileField(
        upload_to='uploaded_files/report',
        default='uploaded_files/report/som.png',
        verbose_name=_('Upload Report'),
        help_text=_('Report file')
    )
# -------------------------- FirstInvoiceStage -------------------------

    date_first_invoice = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date First Invoice'))

    is_paid_first_invoice = models.BooleanField(
        default=False,
        verbose_name=_('Paid First Invoice?'))

    upload_first_invoice = models.FileField(
        upload_to='uploaded_files/firstinvoice',
        default='firstinvoice/som.png',
        verbose_name=_('Upload First Invoice'))

# -------------------------- SecondInvoiceStage -------------------------
    second_invoice = models.ForeignKey(
        SecondInvoiceStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Second invoice')
    )

# -------------------------- LastInvoiceStage -------------------------

    date_last_invoice = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date Last Invoice'))

    is_paid_last_invoice = models.BooleanField(
        default=False,
        verbose_name=_('Paid Last Invoice?'))

    upload_last_invoice = models.FileField(
        upload_to='uploaded_files/lastinvoice',
        default='lastinvoice/som.png',
        verbose_name=_('Upload Last Invoice'))

# -------------------------- OfferStage -------------------------
    date_offer = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date offer'),
        help_text=_('Date when offer was made')
    )

    is_invalid_offer = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Offer?'),
        help_text=_('Check that indicates if offer is incorrect or not')
    )

    is_offer_accepted = models.BooleanField(
        default=False,
        verbose_name=_('Offer accepted?'),
        help_text=_('Check that indicate if client has accepted the project offer')
    )

    upload_offer = models.FileField(
        upload_to='uploaded_files/offer',
        default='uploaded_files/offer/som.png',
        verbose_name=_('Upload Offer'),
        help_text=_('Offer file')
    )

    offer = models.ForeignKey(
        OfferStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Offer data')
    )
# -------------------------- OfferAcceptedStage -------------------------

    offer_accepted = models.ForeignKey(
        OfferAcceptedStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Offer data')
    )

# -------------------------- SignatureStage -------------------------

    signature = models.ForeignKey(
        SignatureStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Signature data')
    )

    date_signature = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date signature'),
        help_text=_('Date when client signed the offer')
    )

    is_signed = models.BooleanField(
        default=False,
        verbose_name=_('Signed contract?'),
        help_text=_('Check that indicates if client has already signed the offer')
    )

    upload_contract = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload Signed Contract'),
        help_text=_('Contract file')
    )

# -------------------------- PermitStage -------------------------
    permit = models.ForeignKey(
        PermitStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Permit data')
    )

    date_permit = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date permit'),
        help_text=_('Date when work permit was uploaded')
    )

    upload_permit = models.FileField(
        upload_to='uploaded_files/permit',
        default='uploaded_files/permit/som.png',
        verbose_name=_('Upload Permit'),
        help_text=_('Work permit file')
    )

    discarded_type = models.CharField(
        choices=ITEM_DISCARDED_TYPES,
        default='Not discarded',
        max_length=50,
        verbose_name=_('Discarded type'),
        help_text=_('Discarded reason for this project')
    )

    date_start_installation = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date start installation'),
        help_text=_('Start date of the installation works')
    )

    is_date_set = models.BooleanField(
        default=False,
        verbose_name=_('Installation date set?'),
        help_text=_('Check that indicates if there is a date set to '
                    'start installation works')
    )

    is_installation_in_progress = models.BooleanField(
        default=False,
        verbose_name=_('Installation in progress?'),
        help_text=_('Check if installation works are in progress')
    )
# -------------------------- DeliveryCertificateStage -------------------------

    upload_delivery_certificate = models.FileField(
        upload_to='uploaded_files/delivery_certificate',
        default='uploaded_files/delivery_certificate/som.png',
        verbose_name=_('Upload delivery certificate'),
        help_text=_('Delivery certificate file')
    )

    date_delivery_certificate = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date delivery certificate'),
        help_text=_('Date when the delivery certificate was issued')
    )

    delivery_certificate = models.ForeignKey(
        DeliveryCertificateStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Delivery certificate')
    )

# -------------------------- LegalRegistrationStage -------------------------
    legal_registration = models.ForeignKey(
        LegalRegistrationStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Legal registration certificate')
    )

    upload_legal_registration_docs = models.FileField(
        upload_to='uploaded_files/legal_registration_docs',
        default='uploaded_files/legal_registration_docs/som.png',
        verbose_name=_('Upload legal registration certificate'))

    date_legal_registration_docs = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date legal registration certificate'),
    )

# -------------------------- LegalitzacionStage -------------------------
    legalization = models.ForeignKey(
        LegalizationStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Legal certificate completed')
    )

    upload_legal_docs = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/som.png',
        verbose_name=_('Upload legal certificate'))

    date_legal_docs = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date legal certificate'),
        help_text=_('Date when legal documentation was uploaded')
    )
# -------------------------- LegalitzacionStage -------------------------

    is_payment_done = models.BooleanField(
        default=False,
        verbose_name=_('Payment done?'),
        help_text=_('Check that indicates if installation is allready paid')
    )

    date_payment_som = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date payment Som Energia'),
        help_text=_('Date of the payment to SomEnergia was done')
    )

    payment_pending = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Payment pending'),
        help_text=_('Amount pending to pay')
    )

    final_payment = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Final payment'),
        help_text=_('Amount of the final payment')
    )

    @transaction.atomic
    def create_prereport_stage(self, date, check, prereport_file):
        self.prereport = PrereportStage.objects.create(
            date=date, check=check, upload=prereport_file
        )
        self.save()

    @transaction.atomic
    def create_report_stage(self, date, check, report_file):
        self.report = ReportStage.objects.create(
            date=date, check=check, upload=report_file
        )
        self.save()

    @transaction.atomic
    def create_second_invoice_stage(self, date, check, second_invoice_file):
        self.second_invoice = SecondInvoiceStage.objects.create(
            date=date, check=check, upload=second_invoice_file
        )
        self.save()

    @transaction.atomic
    def create_offer_stage(self, date, offer_file):
        self.offer = OfferStage.objects.create(
            date=date, upload=offer_file
        )
        self.save()

    @transaction.atomic
    def create_accepted_offer_stage(self, date, check):
        self.offer = OfferStage.objects.create(
            date=date, check=check
        )
        self.save()

    @transaction.atomic
    def create_signature_stage(self, date, check, signature_file):
        self.signature = SignatureStage.objects.create(
            date=date, check=check, upload=signature_file
        )
        self.save()

    @transaction.atomic
    def create_permit_stage(self, date, check, permit_file):
        self.permit = PermitStage.objects.create(
            date=date, check=check, upload=permit_file
        )
        self.save()

    @transaction.atomic
    def create_delivery_certificate_stage(self, date, delivery_cert_file):
        self.delivery_certificateq = DeliveryCertificateStage.objects.create(
            date=date, upload=delivery_cert_file
        )
        self.save()

    @transaction.atomic
    def create_legal_registration_stage(self, date, legal_file):
        self.legal_registration = LegalRegistrationStage.objects.create(
            date=date, upload=legal_file
        )
        self.save()

    @transaction.atomic
    def create_legalization_stage(self, date, rac_file, ritsic_file, cie_file):
        self.legalization = LegalizationStage.objects.create(
            date=date,
            rac_file=rac_file,
            ritsic_file=ritsic_file,
            cie_file=cie_file,
        )
        self.save()

    objects = models.Manager()

    projects = ProjectQuerySet.as_manager()

    def update_is_invalid_prereport(self, is_invalid_prereport):
        self.is_invalid_prereport = is_invalid_prereport
        if self.is_invalid_prereport:
            self.status = 'prereport review'
        else:
            self.status = 'prereport'
        self.save()

    def update_is_invalid_report(self, is_invalid_report):
        self.is_invalid_report = is_invalid_report
        if self.is_invalid_report:
            self.status = 'report review'
        else:
            self.status = 'report'
        self.save()

    def update_upload_prereport(self, upload_prereport):
        self.upload_prereport = upload_prereport
        self.date_prereport = datetime.now().strftime('%Y-%m-%d')
        if not self.is_invalid_prereport:
            self.status = 'prereport'
        self.save()

    def update_upload_report(self, upload_report):
        self.upload_report = upload_report
        self.date_report = datetime.now().strftime('%Y-%m-%d')
        if not self.is_invalid_report:
            self.status = 'report'
        self.save()

    def update_is_paid_first_invoice(self, is_paid_first_invoice):
        self.is_paid_first_invoice = is_paid_first_invoice
        if self.is_paid_first_invoice:
            self.status = 'first payment'
        else:
            self.status = 'pending payment'
        self.save()

    def update_upload_first_invoice(self, upload_first_invoice):
        self.upload_first_invoice = upload_first_invoice
        self.date_first_invoice = datetime.now().strftime('%Y-%m-%d')
        if not self.is_paid_first_invoice:
            self.status = 'pending payment'
        self.save()

    def update_is_paid_last_invoice(self, is_paid_last_invoice):
        self.is_paid_last_invoice = is_paid_last_invoice
        if self.is_paid_last_invoice:
            self.status = 'last payment'
        else:
            self.status = 'pending payment'
        self.save()

    def update_upload_last_invoice(self, upload_last_invoice):
        self.upload_last_invoice = upload_last_invoice
        self.date_last_invoice = datetime.now().strftime('%Y-%m-%d')
        if not self.is_paid_last_invoice:
            self.status = 'pending payment'
        self.save()

    @property
    def technical_visit_dates(self):
        return self.events(manager='events').technical_visit(self)

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name})>'

    def __str__(self):
        return self.name


class Technical_details(models.Model):
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Project'))

    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Campaign'))

    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Client'))

    administrative_division = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Administrative division')
    )

    municipality = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Municipality'),
    )

    street = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Street'),
    )

    town = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Town'),
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('Postal code'),
    )

    contract_number = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('Contract number'),
    )

    cups = models.CharField(
        max_length=22,
        verbose_name=_('CUPS'),
    )

    roof_orientation = models.CharField(
        choices=ITEM_ORIENTATION,
        default='empty',
        max_length=50,
        verbose_name=_('Roof orientation'),
    )

    solar_modules_angle = models.IntegerField(
        choices=ITEM_ANGLES,
        default=0,
        verbose_name=_('Solar models angle'),
    )

    voltage = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('voltage'),
    )

    tariff = models.CharField(
        blank=True,
        max_length=200,
        verbose_name=_('tariff'),
    )

    anual_consumption = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Anual Consumption (kWh)'))

    count_panels = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Solar Panels'))

    installation_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Installation Power (kW)'))

    installation_model = models.CharField(
        blank=True,
        max_length=500)

    installation_singlephase_model = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('installation singlephase model')
    )

    installation_threephase_model = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('installation threephase model')
    )

    shadow_optimizer = models.BooleanField(
        default=False,
        verbose_name=_('shadow optimizer')
    )

    count_shadow_optimizer = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('count shadow optimizer')
    )

    homemanager = models.BooleanField(
        default=False,
        verbose_name=_('homemanager'),
    )

    electric_car = models.BooleanField(
        default=False,
        verbose_name=_('electric car'),
    )

    charger_brand = models.BooleanField(
        default=False,
        verbose_name=_('charger brand'),
    )

    charger_manager = models.BooleanField(
        default=False,
        verbose_name=_('charger manager'),
    )

    electric_car_charger = models.BooleanField(
        default=False,
        verbose_name=_('electric car charger'),
    )

    power_meter = models.BooleanField(
        default=False,
        verbose_name=_('power meter'),
    )

    acquire_interest = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('acquire interest'),
    )

    client_comments = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('client comments'),
    )

    engineering_comments = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('engineering comments'),
    )

    bateries_brand = models.CharField(
        choices=BATERY_BRAND,
        max_length=50,
        default='empty',
        verbose_name=_('batery brand'),
    )

    bateries_model = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('batery model'),
    )

    bateries_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Batery Power (kW)'))

    bateries_capacity = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Batery Capacity (kWh)'))

    bateries_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Batery (€)'),
    )

    shadow_optimizer_brand = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Shadow optimizer brand'),
    )

    shadow_optimizer_model = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Shadow optimizer model'),
    )

    shadow_optimizer_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Shadow Optimizer (€)'))

    peak_power_panels_wp = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Panel Peak Power (Wp)'))

    panel_brand = models.CharField(
        choices=PANELS_BRAND,
        max_length=22,
        default='empty',
        verbose_name=_('Panel brand'),
    )

    panel_type = models.CharField(
        choices=PANELS_TYPE,
        max_length=50,
        default='empty',
        verbose_name=_('Panel type'),
    )

    panel_model = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Panel model'),
    )

    inversor_brand = models.CharField(
        choices=INVERSOR_BRAND,
        max_length=50,
        default='empty',
        verbose_name=_('Inversor brand'),
    )

    inversor_model = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Inversor model'),
    )

    nominal_inversor_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Nominal Inversor Power (Wn)'))

    charger_manager_brand = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Charger manager brand'),
    )

    charger_manager_model = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Charger manager model'),
    )

    charger_manager_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Charger manager (€)'))

    electric_car_charger_brand = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Electric car charger brand'),
    )

    electric_car_charger_model = models.CharField(
        blank=True,
        max_length=22,
        verbose_name=_('Electric car charger model'),
    )

    electric_car_charger_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Electric Car Charger Power (kW)'))

    electric_car_charger_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Electric Car Charger (€)'))

    def __str__(self):
        return self.project.name

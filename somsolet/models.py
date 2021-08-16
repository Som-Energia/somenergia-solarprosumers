from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices_options import (BATERY_BRAND, INVERSOR_BRAND, ITEM_ANGLES,
                              ITEM_COMMUNITY, ITEM_DISCARDED_TYPES,
                              ITEM_ORIENTATION, ITEM_STATUS, ITEM_WARNINGS,
                              LANGUAGES, PANELS_BRAND, PANELS_TYPE)


class LocalGroup(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Name'),
    )

    phone_number = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Telephone number'),
    )

    email = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Email'),
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language'),
    )

    def __str__(self):
        return self.name


class Engineering(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('User'),
    )

    name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Name'),
    )

    tin = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Tax identification number'),
    )

    address = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Address'),
    )

    email = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Email'),
    )

    phone_number = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Telephone number'),
    )

    count_closed_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Campaigns'),
    )

    count_open_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Open Campaigns'),
    )

    count_closed_projects = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Installations'),
    )

    total_kwp_installed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Total kWp installed'),
    )

    comments = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('Comments'),
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language'),
    )

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Name'),
    )

    engineerings = models.ManyToManyField(
        Engineering,
        related_name='campaigns',
        verbose_name=_('Engineering'))

    local_group = models.ManyToManyField(
        LocalGroup,
        related_name='campaigns',
        verbose_name=_('LocalGroup'))

    date_call_for_engineerings = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date call for engineerings'),
    )

    date_call_for_inscriptions = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('date call for inscriptions'),
    )

    date_inscriptions_closed = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date inscriptions closed'),
    )

    date_completed_installations = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date completed installations'),
    )

    autonomous_community = models.CharField(
        choices=ITEM_COMMUNITY,
        default='empty',
        max_length=50,
        verbose_name=_('Autonomous community'),
    )

    geographical_region = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Geographical region'),
    )

    count_foreseen_installations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Number of planned installations'),
    )

    count_completed_installations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Count completed installations'),
    )

    kwp_installed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('kWp installed'),
    )

    date_warranty_payment = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date warranty payment'),
    )

    warranty_pending_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Pending Warranty (€)'),
    )

    warranty_payed_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Payed Warranty (€)'),
    )

    total_penalties_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Total Penalties (days)'),
    )

    total_amount_penalties = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Total Penalties (€)'),
    )

    active = models.BooleanField(
        default=True)

    notify = models.BooleanField(
        default=True)

    def __str__(self):
        return self.name


class Technical_campaign(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        verbose_name=_('Campaign'),
    )

    price_mono_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Monofasic Fixed Price (€)'),
    )

    price_mono_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Monofasic Variable Price (€/Wp)'),
    )

    price_tri_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Trifasic Fixed Price (€)'),
    )

    price_tri_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Trifasic Variable Price (€/Wp)'),
    )

    def __str__(self):
        return self.campaign.name


class ClientFile(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Filename'),
    )

    file = models.FileField(
        upload_to='uploaded_files_som/general_conditions',
        null=True,
        blank=True,
        verbose_name=_('Upload general conditions')
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language')
    )

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Name'),
    )

    membership_number = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Membership number'),
    )

    dni = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('DNI'),
    )

    phone_number = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Telephone number'),
    )

    email = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Email'),
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language'),
    )

    sent_general_conditions = models.BooleanField(
        default=False,
        verbose_name=_('General conditions sent')
    )

    file = models.ManyToManyField(
        ClientFile,
        related_name='clients',
        verbose_name=_('File')
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Installation'))

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

    status = models.CharField(
        choices=ITEM_STATUS,
        default=_('empty status'),
        max_length=50)

    warning = models.CharField(
        choices=ITEM_WARNINGS,
        default=_('No Warn'),
        max_length=100)

    warning_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Warning date'),
    )

    preregistration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Preregistration Date'))

    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('Payed Preregistration'))

    registration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Registration date'),
    )

    is_cch_downloaded = models.BooleanField(
        default=False,
        verbose_name=_('CCH downloaded'))

    date_cch_download = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date CCH downloaded'),
    )

    date_prereport = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date prereport'),
    )

    is_invalid_prereport = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Prereport?'),
    )

    upload_prereport = models.FileField(
        upload_to='uploaded_files/prereport',
        default='uploaded_files/prereport/som.png',
        verbose_name=_('Upload Prereport'),
    )

    date_technical_visit = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date technical visit'),
    )

    date_report = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date report'),
    )

    is_invalid_report = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Report?'))

    upload_report = models.FileField(
        upload_to='uploaded_files/report',
        default='uploaded_files/report/som.png',
        verbose_name=_('Upload Report'))

    date_offer = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date offer'),
    )

    is_invalid_offer = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Offer?'),
    )

    is_offer_accepted = models.BooleanField(
        default=False,
        verbose_name=_('Offer accepted?'),
    )

    upload_offer = models.FileField(
        upload_to='uploaded_files/offer',
        default='uploaded_files/offer/som.png',
        verbose_name=_('Upload Offer'))

    date_signature = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date signature'),
    )

    is_signed = models.BooleanField(
        default=False,
        verbose_name=_('Signed contract?'),
    )

    upload_contract = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload Signed Contract'))

    date_permit = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date permit'),
    )

    upload_permit = models.FileField(
        upload_to='uploaded_files/permit',
        default='uploaded_files/permit/som.png',
        verbose_name=_('Upload Permit'))

    discarded_type = models.CharField(
        choices=ITEM_DISCARDED_TYPES,
        default='Not discarded',
        max_length=50,
        verbose_name=_('Discarded type'),
    )

    date_start_installation = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date start installation'),
    )

    is_date_set = models.BooleanField(
        default=False,
        verbose_name=_('Installtion date set?'),
    )

    is_installation_in_progress = models.BooleanField(
        default=False,
        verbose_name=_('Installation in progress?'),
    )

    upload_delivery_certificate = models.FileField(
        upload_to='uploaded_files/delivery_certificate',
        default='uploaded_files/delivery_certificate/som.png',
        verbose_name=_('Upload delivery certificate'))

    date_delivery_certificate = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date delivery certificate'),
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

    upload_legal_docs = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/som.png',
        verbose_name=_('Upload legal certificate'))

    date_legal_docs = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date legal certificate'),
    )

    is_payment_done = models.BooleanField(
        default=False,
        verbose_name=_('Payment done?'),
    )

    date_payment_som = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date payment Som Energia'),
    )

    payment_pending = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Payment pending'),
    )

    final_payment = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Final payment'),
    )

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


class Mailing(models.Model):

    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )

    notification_status = models.CharField(
        choices=ITEM_STATUS,
        default=_('empty status'),
        max_length=50
    )

    sent = models.BooleanField(
        default=False,
        verbose_name=_('Sent'),
        help_text=_('True if an email was sent')
    )

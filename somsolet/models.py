from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from yamlns import namespace as ns

from .choices_options import (BATERY_BRAND, INVERSOR_BRAND, ITEM_ANGLES,
                              ITEM_COMMUNITY, ITEM_DISCARDED_TYPES,
                              ITEM_ORIENTATION, ITEM_STATUS, ITEM_WARNINGS,
                              PANELS_BRAND, PANELS_TYPE)


class Engineering(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    name = models.CharField(
        blank=True,
        max_length=50)

    tin = models.CharField(
        blank=True,
        max_length=9)

    address = models.CharField(
        blank=True,
        max_length=100)

    email = models.CharField(
        blank=True,
        max_length=50)

    phone_number = models.CharField(
        blank=True,
        max_length=9)

    count_closed_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Campaigns'))

    count_open_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Open Campaigns'))

    count_closed_projects = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Installations'))

    total_kwp_installed = models.FloatField(
        null=True,
        blank=True)

    comments = models.CharField(
        blank=True,
        max_length=500)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(
        blank=True,
        max_length=50)

    engineerings = models.ManyToManyField(
        Engineering,
        related_name='campaigns',
        verbose_name=_('Engineering'))

    date_call_for_engineerings = models.DateField(
        null=True,
        blank=True)

    date_call_for_inscriptions = models.DateField(
        null=True,
        blank=True)

    date_inscriptions_closed = models.DateField(
        null=True,
        blank=True)

    date_completed_installations = models.DateField(
        null=True,
        blank=True)

    autonomous_community = models.CharField(
        choices=ITEM_COMMUNITY,
        default='empty',
        max_length=50)

    geographical_region = models.CharField(
        max_length=50,
        blank=True)

    count_completed_installations = models.IntegerField(
        null=True,
        blank=True)

    kwp_installed = models.FloatField(
        null=True,
        blank=True)

    date_warranty_payment = models.DateField(
        null=True,
        blank=True)

    warranty_pending_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Pending Warranty (€)'))

    warranty_payed_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Payed Warranty (€)'))

    total_penalties_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Total Penalties (days)'))

    total_amount_penalties = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Total Penalties (€)'))

    active = models.BooleanField(
        default=True)

    def __str__(self):
        return self.name


class Technical_campaign(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        verbose_name=_('Campaign'))

    bateries_brand = models.CharField(
        blank=True,
        choices=BATERY_BRAND,
        max_length=50)

    bateries_model = models.CharField(
        blank=True,
        null=True,
        max_length=50)

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
        blank=True)

    shadow_optimizer_brand = models.CharField(
        max_length=50)

    shadow_optimizer_model = models.CharField(
        max_length=22)

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
        max_length=22)

    panel_type = models.CharField(
        choices=PANELS_TYPE,
        max_length=50)

    panel_model = models.CharField(
        max_length=22)

    inversor_brand = models.CharField(
        choices=INVERSOR_BRAND,
        max_length=50)

    inversor_model = models.CharField(
        max_length=50)

    nominal_inversor_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Nominal Inversor Power (Wn)'))

    charger_manager_brand = models.CharField(
        blank=True,
        max_length=22)

    charger_manager_model = models.CharField(
        blank=True,
        max_length=22)

    charger_manager_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Charger manager (€)'))

    electric_car_charger_brand = models.CharField(
        blank=True,
        max_length=22)

    electric_car_charger_model = models.CharField(
        blank=True,
        max_length=22)

    electric_car_charger_power = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Electric Car Charger Power (kW)'))

    electric_car_charger_price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Electric Car Charger (€)'))

    price_mono_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Monofasic Fixed Price (€)'))

    price_mono_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Monofasic Variable Price (€/Wp)'))

    price_tri_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Trifasic Fixed Price (€)'))

    price_tri_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Trifasic Variable Price (€/Wp)'))

    def __str__(self):
        return self.campaign.name


class Client(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100)

    membership_number = models.CharField(
        blank=True,
        max_length=100)

    dni = models.CharField(
        blank=True,
        max_length=9)

    phone_number = models.CharField(
        blank=True,
        max_length=9)

    email = models.CharField(
        blank=True,
        max_length=50)

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
        blank=True)

    preregistration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Preregistration Date'))

    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('Payed Preregistration'))

    registration_date = models.DateField(
        null=True,
        blank=True)

    is_cch_downloaded = models.BooleanField(
        default=False,
        verbose_name=_('CCH downloaded'))

    date_cch_download = models.DateField(
        null=True,
        blank=True)

    date_prereport = models.DateField(
        null=True,
        blank=True)

    is_invalid_prereport = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Prereport?'))

    upload_prereport = models.FileField(
        upload_to='uploaded_files/prereport',
        default='uploaded_files/prereport/som.png',
        verbose_name=_('Upload Prereport'))

    date_technical_visit = models.DateField(
        null=True,
        blank=True)

    date_report = models.DateField(
        null=True,
        blank=True)

    is_invalid_report = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Report?'))

    upload_report = models.FileField(
        upload_to='uploaded_files/report',
        default='uploaded_files/report/som.png',
        verbose_name=_('Upload Report'))

    date_offer = models.DateField(
        null=True,
        blank=True)

    is_invalid_offer = models.BooleanField(
        default=False,
        verbose_name=_('Invalid Offer?'))

    is_offer_accepted = models.BooleanField(
        default=False)

    upload_offer = models.FileField(
        upload_to='uploaded_files/offer',
        default='uploaded_files/offer/som.png',
        verbose_name=_('Upload Offer'))

    date_signature = models.DateField(
        null=True,
        blank=True)

    is_signed = models.BooleanField(
        default=False)

    upload_contract = models.FileField(
        upload_to='uploaded_files/contract',
        default='uploaded_files/contract/som.png',
        verbose_name=_('Upload Signed Contract'))

    date_permit = models.DateField(
        null=True,
        blank=True)

    upload_permit = models.FileField(
        upload_to='uploaded_files/permit',
        default='uploaded_files/permit/som.png',
        verbose_name=_('Upload Permit'))

    discarded_type = models.CharField(
        choices=ITEM_DISCARDED_TYPES,
        default='Not discarded',
        max_length=50)

    date_start_installation = models.DateField(
        null=True,
        blank=True)

    is_date_set = models.BooleanField(
        default=False)

    is_installation_in_progress = models.BooleanField(
        default=False)

    upload_delivery_certificate = models.FileField(
        upload_to='uploaded_files/delivery_certificate',
        default='uploaded_files/delivery_certificate/som.png',
        verbose_name=_('Upload delivery certificate'))

    date_delivery_certificate = models.DateField(
        null=True,
        blank=True)

    upload_legal_docs = models.FileField(
        upload_to='uploaded_files/legal_docs',
        default='uploaded_files/legal_docs/som.png',
        verbose_name=_('Upload legal certificate'))

    date_legal_docs = models.DateField(
        null=True,
        blank=True)

    is_payment_done = models.BooleanField(
        default=False)

    date_payment_som = models.DateField(
        null=True,
        blank=True)

    payment_pending = models.FloatField(
        null=True,
        blank=True)

    final_payment = models.FloatField(
        null=True,
        blank=True)

    def prereport_review(
            self,
            date_prereport_review,
            member_id,
            contract_id,
            campaign_id,
            is_invalid_prereport,):
        self.is_invalid_prereport = is_invalid_prereport
        self.date_prereport = date_prereport_review
        if is_invalid_prereport:
            self.status = 'discarded'
            self.discarded_type = 'technical'
        else:
            self.status = 'prereport'

    def report_review(
            self,
            date_report_review,
            member_id,
            contract_id,
            campaign_id,
            is_invalid_report,):
        self.is_invalid_report = is_invalid_report
        self.date_report = date_report_review
        if is_invalid_report:
            self.status = 'discarded'
            self.discarded_type = 'technical'
        else:
            self.status = 'report'

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
        blank=True)

    municipality = models.CharField(
        max_length=50,
        blank=True)

    street = models.CharField(
        max_length=50,
        blank=True)

    town = models.CharField(
        max_length=50,
        blank=True)

    postal_code = models.CharField(
        max_length=10,
        blank=True)

    contract_number = models.CharField(
        max_length=10,
        blank=True)

    cups = models.CharField(
        max_length=22)

    roof_orientation = models.CharField(
        choices=ITEM_ORIENTATION,
        default='empty',
        max_length=50)

    solar_modules_angle = models.IntegerField(
        choices=ITEM_ANGLES,
        default=0)

    voltage = models.CharField(
        blank=True,
        max_length=50)

    tariff = models.CharField(
        null=True,
        blank=True,
        max_length=200)

    anual_consumption = models.CharField(
        null=True,
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
        null=True,
        blank=True,
        max_length=500)

    installation_singlephase_model = models.CharField(
        null=True,
        blank=True,
        max_length=500)

    installation_threephase_model = models.CharField(
        null=True,
        blank=True,
        max_length=500)

    shadow_optimizer = models.BooleanField(
        default=False)

    count_shadow_optimizer = models.IntegerField(
        null=True,
        blank=True)

    homemanager = models.BooleanField(
        default=False)

    electric_car = models.BooleanField(
        default=False)

    charger_brand = models.BooleanField(
        default=False)

    charger_manager = models.BooleanField(
        default=False)

    electric_car_charger = models.BooleanField(
        default=False)

    power_meter = models.BooleanField(
        default=False)

    acquire_interest = models.CharField(
        null=True,
        blank=True,
        max_length=500)

    client_comments = models.CharField(
        null=True,
        blank=True,
        max_length=500)

    engineering_comments = models.CharField(
        null=True,
        blank=True,
        max_length=500)

    def __str__(self):
        return self.project.name

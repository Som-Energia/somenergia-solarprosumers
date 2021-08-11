from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from .campaign import CampaignFactory
from .client import ClientFactory
from .admin import EngineeringFactory, InventsPacoEngineeringFactory

from .stages import (SignatureFileFactory, SignatureFileBaseFactory, PermitFileFactory,
                     LegalRegistrationFileBaseFactory, LegalRegistrationFileFactory,
                     LegalizationFileFactory, PrereportFileFactory, OfferFileFactory)



class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Project'

    name = 'Instalació plaques Montserrat Escayola'
    campaign = factory.SubFactory(CampaignFactory)
    client = factory.SubFactory(ClientFactory)
    engineering = factory.SubFactory(InventsPacoEngineeringFactory)
    status = 'empty status'
    warning = 'No Warn'
    warning_date = None
    preregistration_date = None
    is_paid = False
    registration_date = None
    is_cch_downloaded = False
    date_cch_download = None
    prereport = factory.SubFactory(PrereportFileFactory)
    date_technical_visit = factory.Faker('date_time')
    date_report = None
    is_invalid_report = False
    upload_report = False
    date_first_invoice = None
    is_paid_first_invoice = False
    upload_first_invoice = None
    date_last_invoice = None
    is_paid_last_invoice = False
    upload_last_invoice = None
    date_offer = None
    is_invalid_offer = False
    is_offer_accepted = False
    upload_offer = None
    signature = factory.SubFactory(SignatureFileBaseFactory)
    permit = factory.SubFactory(PermitFileFactory)
    date_permit = None
    offer= factory.SubFactory(OfferFileFactory)
    discarded_type = 'Not discarded'
    date_start_installation = None
    is_date_set = False
    is_installation_in_progress = False
    upload_delivery_certificate = None
    date_delivery_certificate = None
    legal_registration = factory.SubFactory(LegalRegistrationFileBaseFactory)
    legalization = factory.SubFactory(LegalizationFileFactory)
    is_payment_done = False
    date_payment_som = None
    payment_pending = 2000
    final_payment = 6000


class ProjectStageFactory(ProjectFactory):
    signature = factory.SubFactory(SignatureFileFactory)
    legal_registration = factory.SubFactory(LegalRegistrationFileFactory)


class TechnicalDetailsFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Technical_details'

    project = factory.SubFactory(ProjectFactory)
    campaign = factory.SubFactory(CampaignFactory)
    client = factory.SubFactory(ClientFactory)
    administrative_division = 'Barbados'
    municipality = 'Parroquia de Christ Church'
    street = 'Bridgetown Norman'
    town = 'Speightstown'
    postal_code = '08026'
    contract_number = '12345'
    cups = 'ES0024123453789101XXYY'
    roof_orientation = 'empty'
    solar_modules_angle = 0
    voltage = '120'
    tariff = '2.0A'
    anual_consumption = '12000'
    count_panels = '10'
    installation_power = '110'
    installation_model = 'Jinko'
    installation_singlephase_model = 'Jinko-1000'
    installation_threephase_model = 'Jinko-S1000'
    shadow_optimizer = True
    count_shadow_optimizer = '5'
    homemanager = True
    electric_car = True
    charger_brand = True
    charger_manager = True
    electric_car_charger = True
    power_meter = True
    acquire_interest = 'Bateries, optimitzador de ombres'
    client_comments = 'Gràcies, sou molt macus'
    engineering_comments = ''
    bateries_brand = 'Toni Chargers'
    bateries_model = 'LT-3000 v5.4'
    bateries_power = '3000'
    bateries_capacity = '15000'
    bateries_price = '3000'
    shadow_optimizer_brand = 'Rasillo SolarTrade Ltd.'
    shadow_optimizer_model = 'SO V4-T54'
    shadow_optimizer_price = '300'
    peak_power_panels_wp = '3500'
    panel_brand = 'Ras SolarTrade Ltd.'
    panel_type = 'CRISTAL'
    panel_model = 'SP2 High Performance 3'
    inversor_brand = 'Rasillo SolarTrade Ltd.'
    inversor_model = 'RJ78 Inverter Plus'
    nominal_inversor_power = '300'
    charger_manager_brand = 'Toni Chargers'
    charger_manager_model = 'Car Charger 2000 T2-v7'
    charger_manager_price = '300'
    electric_car_charger_brand = 'Toni Chargers'
    electric_car_charger_model = 'Ultra Fast Charger 5v2'
    electric_car_charger_power = '1500'
    electric_car_charger_price = '2000'

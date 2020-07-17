from datetime import datetime
import factory
from factory.django import DjangoModelFactory

from .campaign import CampaignFactory
from .client import ClientFactory


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Project'

    name = 'Instalació plaques Montserrat Escayola'
    campaign = factory.RelatedFactory(CampaignFactory)
    client = factory.RelatedFactory(ClientFactory)
    status = 'empty status'
    warning = 'No Warn'
    warning_date = None
    preregistration_date = None
    is_paid = False
    registration_date = None
    is_cch_downloaded = False
    date_cch_download = None
    date_prereport = None
    is_invalid_prereport = False
    upload_prereport = None
    date_technical_visit = datetime(2020, 8, 7)
    date_report = False
    is_invalid_report = False
    upload_report = False
    date_offer = None
    is_invalid_offer = False
    is_offer_accepted = False
    upload_offer = None
    date_signature = None
    is_signed = False
    upload_contract = None
    date_permit = None
    discarded_type = 'Not discarded'
    date_start_installation = None
    is_date_set = False
    is_installation_in_progress = False
    upload_delivery_certificate = None
    date_delivery_certificate = None
    upload_legal_registration_docs = None
    date_legal_registration_docs = None
    upload_legal_docs = None
    date_legal_docs = None
    is_payment_done = False
    date_payment_som = None
    payment_pending = 2000
    final_payment = 6000


class TechnicalDetailsFactory(DjangoModelFactory):
    
    class Meta:
        model = 'somsolet.Technical_details'    

    project = factory.RelatedFactory(ProjectFactory)
    campaign = factory.RelatedFactory(CampaignFactory)
    client = factory.RelatedFactory(ClientFactory)
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
    panel_brand = 'Rasillo SolarTrade Ltd.'
    panel_type = 'CRISTAL'
    panel_model = 'SP210 High Performance 3'
    inversor_brand = 'Rasillo SolarTrade Ltd.'
    inversor_model = 'RJ78 Inverter Plus'
    nominal_inversor_power = '300'
    charger_manager_brand = 'Toni Chargers'
    charger_manager_model = 'Car Charger Manager 2000 T23-v7'
    charger_manager_price = '300'
    electric_car_charger_brand = 'Toni Chargers'
    electric_car_charger_model = 'Ultra Fast Car Charger 57v2'
    electric_car_charger_power = '1500'
    electric_car_charger_price = '2000'
import factory
from factory.django import DjangoModelFactory

from .admin import InventsPacoEngineeringFactory
from .campaign import CampaignFactory
from .client import ClientFactory
from .admin import InventsPacoEngineeringFactory

from .stages import (SignatureStageFactory, SignatureStageBaseFactory, PermitStageFactory,
                     LegalRegistrationStageBaseFactory, LegalRegistrationStageFactory,
                     LegalizationStageFactory, PrereportStageFactory, ReportStageFactory,
                     ReportBaseStageFactory, OfferStageFactory, OfferBaseStageFactory,
                     OfferAcceptedStageFactory, SecondInvoiceStageFactory, DeliveryCertificateStageFactory,
                     FirstInvoiceStageFactory)



class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Project'
        django_get_or_create = ('name', )

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
    prereport = factory.SubFactory(PrereportStageFactory)
    date_technical_visit = factory.Faker('date_time')
    report = factory.SubFactory(ReportBaseStageFactory)
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
    signature = factory.SubFactory(SignatureStageBaseFactory)
    first_invoice = factory.SubFactory(FirstInvoiceStageFactory)
    permit = factory.SubFactory(PermitStageFactory)
    date_permit = None
    offer = factory.SubFactory(OfferBaseStageFactory)
    offer_accepted = factory.SubFactory(OfferAcceptedStageFactory)
    second_invoice = factory.SubFactory(SecondInvoiceStageFactory)
    discarded_type = 'Not discarded'
    date_start_installation = None
    is_date_set = False
    is_installation_in_progress = False
    upload_delivery_certificate = None
    date_delivery_certificate = None
    delivery_certificate = factory.SubFactory(DeliveryCertificateStageFactory)
    legal_registration = factory.SubFactory(LegalRegistrationStageBaseFactory)
    legalization = factory.SubFactory(LegalizationStageFactory)
    is_payment_done = False
    date_payment_som = None
    payment_pending = 2000
    final_payment = 6000


class ProjectStageFactory(ProjectFactory):
    report = factory.SubFactory(ReportStageFactory)
    offer = factory.SubFactory(OfferStageFactory)
    signature = factory.SubFactory(SignatureStageFactory)
    legal_registration = factory.SubFactory(LegalRegistrationStageFactory)
 

class ProjectEmptyStatusStageFactory(ProjectFactory):
    id = 1
    status = 'empty status'


class ProjectPrereportRegisteredStageFactory(ProjectFactory):
    id = 1
    status = 'registered'


class ProjectPrereportStageFactory(ProjectFactory):
    id = 1
    status = 'prereport'


class ProjectSignatureStageFactory(ProjectFactory):
    id = 1
    status = 'offer accepted'


class ProjectFirstInvoiceStageFactory(ProjectFactory):
    id = 1
    status = 'signature'


class ProjectPermitStageFactory(ProjectFactory):
    id = 1
    status = 'signature'


class ProjectOfferStageFactory(ProjectFactory):
    id = 1
    status = 'report'


class ProjectOfferAcceptedStageFactory(ProjectFactory):
    id = 1
    status = 'offer review'


class ProjectSecondInvoiceStageFactory(ProjectFactory):
    id = 1
    status = 'end installation'


class ProjectLegalRegistrationStageFactory(ProjectFactory):
    id = 1
    status = 'end installation'


class ProjectLegalizationStageFactory(ProjectFactory):
    id = 1
    status = 'last payment'


class ProjectDeliveryCertificateStageFactory(ProjectFactory):
    id = 1
    status = 'date installation set'


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

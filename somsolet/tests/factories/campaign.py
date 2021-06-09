from datetime import date

import factory
from factory.django import DjangoModelFactory

from .admin import InventsPacoEngineeringFactory, LocalGroupFactory


class CampaignFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Campaign'
        django_get_or_create = ('name', )

    name = 'Solar Paco'
    engineerings = factory.RelatedFactory(InventsPacoEngineeringFactory)
    local_group = factory.RelatedFactory(LocalGroupFactory)
    date_call_for_engineerings = factory.Faker(
        'date_object',
    )
    date_call_for_inscriptions = factory.Faker(
        'date_between_dates',
        date_start=factory.SelfAttribute('..date_call_for_engineerings')
    )
    date_inscriptions_closed = None
    date_completed_installations = None
    autonomous_community = 'Parroquia de Christ Church'
    geographical_region = 'Barbados'
    count_foreseen_installations = 400
    count_completed_installations = 0
    kwp_installed = 0
    date_warranty_payment = None
    warranty_pending_amount = 0
    warranty_payed_amount = 0
    total_penalties_days = 0
    total_amount_penalties = 0
    active = True


class TechnicalCampaignFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Technical_campaign'

    campaign = factory.RelatedFactory(CampaignFactory)
    price_mono_fixed = '0.5'
    price_mono_var = '0.1'
    price_tri_fixed = '0.3'
    price_tri_var = '0.7'

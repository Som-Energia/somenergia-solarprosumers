from factory import RelatedFactory

from factory.django import DjangoModelFactory
from .admin import LocalGroupFactory, EngineeringFactory

class CampaignFactory(DjangoModelFactory):

    class Meta:
        model = 'somsolet.Campaign'

    name = 'Solar Paco'
    engineerings = RelatedFactory(EngineeringFactory)
    local_group = RelatedFactory(LocalGroupFactory)
    date_call_for_engineerings = '2020-01-01'
    date_call_for_inscriptions = '2020-02-02'
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

    campaign = RelatedFactory(CampaignFactory)
    price_mono_fixed = '0.5'
    price_mono_var = '0.1'
    price_tri_fixed = '0.3'
    price_tri_var = '0.7'

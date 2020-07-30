import pytest

from . import factories


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():

        engineering_user = factories.UserFactory()
        engineering_user.save()
        local_group = factories.LocalGroupFactory()
        local_group.save()
        engineering = factories.EngineeringFactory()
        engineering.save()

        campaign = factories.CampaignFactory()
        campaign.engineerings.set((engineering,))
        campaign.local_group.set((local_group,))
        campaign.save()
        technical_campaign = factories.TechnicalCampaignFactory()
        print(technical_campaign.__dict__)
        import pdb; pdb.set_trace()

        technical_campaign.campaign.set(campaign)
        technical_campaign.save()

        project = factories.ProjectFactory()
        project.campaign = campaign
        project.save()

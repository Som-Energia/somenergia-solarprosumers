import pytest

from factory import RelatedFactory, SubFactory

from .factories import (CampaignFactory, ClientFactory, EngineeringFactory, InventsPacoEngineeringFactory,
                        ProjectFactory, TechnicalDetailsFactory, UserFactory, LocalGroupFactory,
                        MailingFactory)

__all__ = (
    'engineering_user', 'engineering', 'campaign__solar_paco',
    'technical_details', 'project', 'client', 'local_group', 'mailing_signature',
    'mailing_legal_registration'
)


@pytest.fixture
def engineering_user(db):
    return UserFactory()


@pytest.fixture
def engineering(db):
    return EngineeringFactory()


@pytest.fixture
def campaign__solar_paco(db):
    campaign = CampaignFactory.build()
    campaign.save()
    campaign.engineerings.add(InventsPacoEngineeringFactory())
    return campaign


@pytest.fixture
def technical_details(db):
    return TechnicalDetailsFactory()


@pytest.fixture
def project(db):
    return ProjectFactory()


@pytest.fixture
def client(db):
    return ClientFactory()


@pytest.fixture
def local_group(db):
    return LocalGroupFactory()

@pytest.fixture
def mailing_signature(db):
    mailing = MailingFactory()
    mailing.notification_status = 'signature'
    mailing.save()
    return mailing

@pytest.fixture
def mailing_legal_registration(db):
    mailing = MailingFactory()
    mailing.notification_status = 'legal_registration'
    mailing.save()
    return mailing
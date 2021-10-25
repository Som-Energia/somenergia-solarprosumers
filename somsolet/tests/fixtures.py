import pytest

from .factories import (CampaignFactory, ClientFactory, EngineeringFactory,
                        InventsPacoEngineeringFactory, InventsPacoFactory,
                        LocalGroupFactory, ProjectFactory,
                        TechnicalDetailsFactory, UserFactory, MailingFactory)

__all__ = (
    'engineering_user', 'engineering',
    'technical_details', 'project', 'client', 'local_group', 'mailing_signature',
    'mailing_legal_registration', 'mailing_offer'
)


@pytest.fixture
def engineering_user(db):
    return UserFactory()


@pytest.fixture
def engineering_user_paco(db):
    return InventsPacoFactory.create()


@pytest.fixture
def engineering(db):
    return EngineeringFactory()


@pytest.fixture
def engineering__solar_paco(db):
    return InventsPacoEngineeringFactory.create()


@pytest.fixture
def campaing__solar_paco(db):
    return CampaignFactory()


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

@pytest.fixture
def mailing_offer(db):
    mailing = MailingFactory()
    mailing.notification_status = 'offer'
    mailing.save()
    return mailing
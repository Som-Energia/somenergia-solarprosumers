import pytest

from .factories import (CampaignFactory, ClientFactory, EngineeringFactory,
                        ProjectFactory, TechnicalDetailsFactory, UserFactory)


@pytest.fixture
def engenieering_user(db):
    return UserFactory()


@pytest.fixture
def engenieering(db):
    return EngineeringFactory()


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

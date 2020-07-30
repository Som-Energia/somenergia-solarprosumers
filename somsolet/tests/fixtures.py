import pytest

from .factories import (CampaignFactory, ClientFactory, EngineeringFactory,
                        ProjectFactory, TechnicalDetailsFactory, UserFactory, LocalGroupFactory)


@pytest.fixture
def engenieering_user(db):
    return UserFactory()


@pytest.fixture
def engineering(db):
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


@pytest.fixture
def local_group(db):
    return LocalGroupFactory()

import pytest
from .factories import (CampaignFactory, EngineeringFactory,
                        TechnicalDetailsFactory, UserFactory)

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

import psycopg2
import pytest
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .factories import (CampaignFactory, EngineeringFactory,
                        TechnicalDetailsFactory, UserFactory)


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


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

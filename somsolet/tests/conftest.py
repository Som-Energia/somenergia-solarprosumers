import psycopg2
import pytest
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .factories import CampaignFactory, TechnicalDetailsFactory, UserFactory


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'somsolet4test_db'

    run_sql('DROP DATABASE IF EXISTS somsolet4test_db')
    run_sql('CREATE DATABASE somsolet4test_db TEMPLATE somsolet_db')

    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE somsolet4test_db')


@pytest.fixture
def campaing__solar_paco(db):
    return CampaignFactory()


@pytest.fixture
def technical_details(db):
    return TechnicalDetailsFactory()


@pytest.fixture
def ingenieering_user(db):
    return UserFactory
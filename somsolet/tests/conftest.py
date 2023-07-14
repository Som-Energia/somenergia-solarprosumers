import psycopg2
import pytest

from django.db import connections
from django.conf import settings

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(
        database="postgres",
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"]["NAME"] = "somsolet4test_db"

    run_sql("DROP DATABASE IF EXISTS somsolet4test_db")
    run_sql("CREATE DATABASE somsolet4test_db TEMPLATE somsolet_db")

    yield

    for connection in connections.all():
        connection.close()

    run_sql("DROP DATABASE somsolet4test_db")

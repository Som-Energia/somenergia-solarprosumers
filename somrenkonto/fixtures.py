import pytest

from somsolet.tests.factories import SolarWindPowerEngineeringFactory
from somsolet.tests.fixtures import engineering_user_paco, project
from .factories import *
from faker.factory import Factory

Faker = Factory.create


@pytest.fixture
def technical_visit_event():
    return TechnicalVisitEventFactory.create()


@pytest.fixture
def calendar_config_month_view():
    return CalendarConfigMonthViewFactory.create()


@pytest.fixture
def calendar_with_conf(calendar_config_month_view, engineering_user_paco):
    calendar = calendar_config_month_view.calendar
    calendar.create_relation(engineering_user_paco)
    return calendar


@pytest.fixture
def calendar(calendar_with_conf, project):
    return calendar_with_conf


@pytest.fixture
def engineering_with_events(technical_visit_event):
    return technical_visit_event.engineering


@pytest.fixture
def engineering_without_events():
    return SolarWindPowerEngineeringFactory.create()

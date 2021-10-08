import pytest
from datetime import datetime, timedelta
from django.utils import timezone

from somsolet.tests.factories import SolarWindPowerEngineeringFactory
from somsolet.tests.fixtures import engineering_user_paco, project
from .factories import *
from somsolet.tests.factories import (CampaignFactory,
                                      InventsPacoEngineeringFactory,
                                      ProjectFactory)
from .models import EventChoices
from faker.factory import Factory

Faker = Factory.create


@pytest.fixture
def technical_visit_event():
    return TechnicalVisitEventFactory.create()


@pytest.fixture
def technical_visit_event_request():
    calendar = CalendarFactory()
    campaign = CampaignFactory()
    project = ProjectFactory()
    engineering = InventsPacoEngineeringFactory()

    fake = Faker()
    fake.seed(0)
    tz = timezone.get_current_timezone()
    start = fake.date_time_between(tzinfo=tz)
    end = start + timedelta(minutes=60)

    return dict(
        title='Visita técnica',
        description='Visita técnica per evaluar si es poden posar plaques solars',
        start=datetime.strftime(start, '%Y-%m-%dT%H:%M:%S%z'),
        end=datetime.strftime(end, '%Y-%m-%dT%H:%M:%S%z'),
        all_day=False,
        calendar=calendar.id,
        event_type=EventChoices.TECHNICAL_VISIT,
        campaign=campaign.id,
        project=project.id,
        engineering=engineering.id,
    )


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

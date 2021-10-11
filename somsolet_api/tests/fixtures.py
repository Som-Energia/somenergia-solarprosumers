from datetime import datetime, timedelta

import factory
import pytest
from django.contrib.auth import authenticate
from django_currentuser.middleware import _set_current_user
from django.utils import timezone

from somrenkonto.fixtures import *
from somrenkonto.factories import (CalendarFactory, CampaignFactory,
                                   ProjectFactory, RenkontoEventFactory)
from somrenkonto.models import EventChoices
from somsolet.tests.factories import (InventsPacoEngineeringFactory,
                                      InventsPacoFactory,
                                      SolarWindPowerEngineeringFactory,
                                      SuperuserFactory)

from .factories import TechnicalVisitDataFactory


@pytest.fixture
def authenticated_user():
    user = InventsPacoFactory.create()
    user_authenticated = authenticate(username=user.username, password="1234")

    _set_current_user(user_authenticated)
    return user_authenticated


@pytest.fixture
def authenticated_superuser():
    user = SuperuserFactory.create()
    user_authenticated = authenticate(username=user.username, password="1234")

    _set_current_user(user_authenticated)
    return user_authenticated


@pytest.fixture
def bounded_event():
    created_by = factory.SubFactory(InventsPacoFactory)
    bounded_event_data = dict(
        title='Super urgent meet',
        description='Meet with Durruti and Bakunin to plan some revolutions',
        start=factory.Faker(
            'date_time_between_dates',
            datetime_start=timezone.make_aware(datetime(2020, 1, 1, 12, 5)),
            datetime_end=timezone.localtime(),
            tzinfo=timezone.get_current_timezone()
        ),
        end=factory.Faker(
            'date_time_between_dates',
            datetime_start=factory.SelfAttribute('..start'),
            tzinfo=timezone.get_current_timezone()
        ),
        all_day=False,
        event_type=EventChoices.UNAVAILABILITY,
        calendar=factory.SubFactory(CalendarFactory),
        campaign=factory.SubFactory(CampaignFactory),
        project=factory.SubFactory(ProjectFactory),
        engineering=factory.SubFactory(InventsPacoEngineeringFactory),
        created_by=created_by,
        modified_by=created_by
    )
    return RenkontoEventFactory.create(**bounded_event_data)


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
        date_start=datetime.strftime(start, '%Y-%m-%dT%H:%M:%S%z'),
        date_end=datetime.strftime(end, '%Y-%m-%dT%H:%M:%S%z'),
        all_day=False,
        calendar=calendar.id,
        event_type=EventChoices.TECHNICAL_VISIT,
        campaign=campaign.id,
        project=project.id,
        engineering=engineering.id,
    )


@pytest.fixture
def technical_event():
    return TechnicalVisitDataFactory.data_ok()


@pytest.fixture
def engineering():
    return SolarWindPowerEngineeringFactory.create()


@pytest.fixture
def montse_project():
    return ProjectFactory.create()


@pytest.fixture
def engineering_with_events():
    engineering = InventsPacoEngineeringFactory.create()

    bounded_event_data = dict(
        title=factory.Iterator([
            'Super urgent meet',
            'Meeting with Escayola',
            'Vacations'
        ]),
        description=factory.Iterator([
            'Meet with Durruti and Bakunin to plan some revolutions',
            'Lorem fistrum no puedor qué dise usteer al ataquerl ',
            'Ese que llega quietooor llevame al sircoo por la gloria de mi madre'
        ]),
        start=factory.Faker(
            'date_time_between_dates',
            datetime_start=timezone.make_aware(datetime(2020, 1, 1, 12, 5)),
            datetime_end=timezone.localtime(),
            tzinfo=timezone.get_current_timezone()
        ),
        end=factory.Faker(
            'date_time_between_dates',
            datetime_start=factory.SelfAttribute('..start'),
            tzinfo=timezone.get_current_timezone()
        ),
        all_day=False,
        event_type=EventChoices.UNAVAILABILITY,
        calendar=factory.SubFactory(CalendarFactory),
        campaign=factory.SubFactory(CampaignFactory),
        project=factory.SubFactory(ProjectFactory),
        engineering=engineering,
        created_by=factory.SubFactory(InventsPacoFactory),
        modified_by=factory.SubFactory(InventsPacoFactory)
    )

    RenkontoEventFactory.create_batch(
        size=5, **bounded_event_data
    )

    return engineering


@pytest.fixture
def stats():
    stats_data = dict(
        total_instalations=10,
        total_power=dict(
            value=30,
            units='kWp'
        ),
        total_generation=dict(
            value=0.0435,
            units='GWp/any'
        )
    )
    return stats_data

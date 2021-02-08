from datetime import datetime

import factory
import pytest
from django.utils import timezone

from somsolet.tests.factories import UserFactory, EngineeringFactory
from somrenkonto.factories import RenkontoEventFactory, CalendarFactory, CampaignFactory, ProjectFactory

from somrenkonto.models import EventChoices

@pytest.fixture
def bounded_event():
    created_by = factory.SubFactory(UserFactory)
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
        created_by=created_by,
        modified_by=created_by
    )

    return RenkontoEventFactory.build(**bounded_event_data)


@pytest.fixture
def authenticated_user():
    return UserFactory.create()


@pytest.fixture
def engineering():
    return EngineeringFactory.create()
from datetime import datetime

import factory
import pytest

from somsolet.tests.factories import UserFactory
from somrenkonto.factories import RenkontoEventFactory, CalendarFactory, CampaignFactory, ProjectFactory

from somrenkonto.models import EventChoices

@pytest.fixture
def bounded_event():
    created_by = factory.SubFactory(UserFactory)
    bounded_event_data = dict(
        title='Super urgent meet',
        description='Meet with Durruti and Bakunin to plan some revolutions',
        start=factory.Faker(
            'date_between_dates',
            date_start=datetime(2020, 1, 1, 12, 5)
        ),
        end=factory.Faker(
        'date_between_dates',
        date_start=factory.SelfAttribute('..start')
        ),
        all_day=False,
        event_type=EventChoices.UNAVAILABILITY,
        calendar=factory.SubFactory(CalendarFactory),
        campaign=factory.SubFactory(CampaignFactory),
        project=factory.SubFactory(ProjectFactory),
        created_by=created_by,
        modified_by=created_by
    )

    return RenkontoEventFactory(**bounded_event_data)


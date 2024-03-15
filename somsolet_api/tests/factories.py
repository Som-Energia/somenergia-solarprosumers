from datetime import datetime, timedelta
from django.utils import timezone

import factory
from faker.factory import Factory

from somrenkonto.factories import CalendarFactory, CampaignFactory, ProjectFactory
from somsolet.tests.factories import InventsPacoEngineeringFactory
from somrenkonto.models import EventChoices


Faker = Factory.create


class TechnicalVisitDataFactory(factory.StubFactory):
    @staticmethod
    def data_ok():
        fake = Faker()
        fake.seed(0)
        tz = timezone.get_current_timezone()
        start = fake.date_time_between(tzinfo=tz)
        end = start + timedelta(minutes=60)

        return {
            "date_start": datetime.strftime(start, "%Y-%m-%dT%H:%M:%S%z"),
            "date_end": datetime.strftime(end, "%Y-%m-%dT%H:%M:%S%z"),
        }


class TechnicalVisitRequestDataFactory(factory.StubFactory):
    @staticmethod
    def data_ok():
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
            title="Visita técnica",
            description="Visita técnica per evaluar si es poden posar plaques solars",
            date_start=datetime.strftime(start, "%Y-%m-%dT%H:%M:%S%z"),
            date_end=datetime.strftime(end, "%Y-%m-%dT%H:%M:%S%z"),
            all_day=False,
            calendar=calendar.id,
            event_type=EventChoices.TECHNICAL_VISIT,
            campaign=campaign.id,
            project=project.id,
            engineering=engineering.id,
        )

from datetime import datetime, timedelta
from django.utils import timezone

import factory
from faker.factory import Factory

Faker = Factory.create


class TechnicalVisitDataFactory(factory.StubFactory):

    def data_ok():
        fake = Faker()
        fake.seed(0)
        start = timezone.now()
        tz = timezone.get_current_timezone()
        start = fake.date_time_between(tzinfo=tz)
        end = start + timedelta(minutes=60)

        return {
            'date_start': datetime.strftime(start, '%Y-%m-%dT%H:%M:%S%z'),
            'date_end': datetime.strftime(end, '%Y-%m-%dT%H:%M:%S%z'),

        }

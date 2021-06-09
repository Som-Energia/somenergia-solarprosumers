from datetime import datetime, timedelta

import factory
from faker.factory import Factory

Faker = Factory.create


class TechnicalVisitDataFactory(factory.StubFactory):

    def data_ok():
        fake = Faker()
        fake.seed(0)
        start = fake.future_datetime()

        return {
            'dateStart': fake.iso8601(end_datetime=start),
            'dateEnd': fake.iso8601(end_datetime=start + timedelta(minutes=60))
        }

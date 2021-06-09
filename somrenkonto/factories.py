from datetime import datetime, timedelta

import factory
from django.utils import timezone as tz
from schedule.models import Calendar

from somsolet.tests.factories import (CampaignFactory,
                                      InventsPacoEngineeringFactory,
                                      InventsPacoFactory, ProjectFactory,
                                      UserFactory)

from .models import (CalendarConfig, CalendarViewChoices, EventChoices,
                     RenkontoEvent)

__all__ = (
    'CalendarFactory',
    'CalendarConfigFactory',
    'CalendarConfigMonthViewFactory',
    'RenkontoEventFactory',
    'TechnicalVisitEventFactory'
)


class CalendarFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Calendar
        django_get_or_create = ('slug',)

    name = 'Calendario Obras Ingenieria Invents Paco i asociats'
    slug = 'cal-obras-ing'


class CalendarConfigFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CalendarConfig

    calendar = factory.SubFactory(CalendarFactory)

    created_by = factory.SubFactory(InventsPacoFactory)

    modified_by = factory.SubFactory(InventsPacoFactory)


class CalendarConfigMonthViewFactory(CalendarConfigFactory):

    default_calendar_view = CalendarViewChoices.MONTH_VIEW


class RenkontoEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = RenkontoEvent


class TechnicalVisitEventFactory(RenkontoEventFactory):
    title = 'Visita técnica'

    description = 'Visita técnica per evaluar si es poden posar plaques solars'

    start = factory.Faker(
        'date_time_between_dates',
        datetime_end=tz.make_aware(datetime.now() + timedelta(days=3)),
    )
    end = factory.Faker(
        'date_time_between_dates',
        datetime_start=factory.SelfAttribute('..start'),
        datetime_end=factory.LazyAttribute(
            lambda self: tz.make_aware(self.datetime_start + timedelta(hours=2))
        ),
    )

    all_day = False

    calendar = factory.SubFactory(CalendarFactory)

    event_type = EventChoices.TECHNICAL_VISIT

    campaign = factory.SubFactory(CampaignFactory)

    project = factory.SubFactory(ProjectFactory)

    engineering = factory.SubFactory(InventsPacoEngineeringFactory)

    created_by = factory.SubFactory(UserFactory)

    modified_by = factory.SubFactory(UserFactory)

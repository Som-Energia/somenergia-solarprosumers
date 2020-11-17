from factory.django import DjangoModelFactory
from schedule.models import Calendar
from somsolet.tests.factories import UserFactory


class CalendarFactory(DjangoModelFactory):
    
    class Meta:
        model = Calendar

    name = 'Calendario Obras Ingenieria Invents Paco i asociats'
    slug = 'cal-obras-ing'

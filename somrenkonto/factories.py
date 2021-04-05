from datetime import datetime

import factory
from schedule.models import Calendar

from somsolet.tests.factories import UserFactory, CampaignFactory, ProjectFactory
from .models import RenkontoEvent, EventChoices


class CalendarFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Calendar

    name = 'Calendario Obras Ingenieria Invents Paco i asociats'
    slug = 'cal-obras-ing'


class RenkontoEventFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = RenkontoEvent
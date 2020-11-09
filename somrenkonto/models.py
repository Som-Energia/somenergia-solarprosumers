import json
from datetime import datetime, time

from django.db import models
from django.core import serializers
from django.utils.translation import gettext_lazy as _
from schedule.models import Calendar, Event

from somsolet.models import Campaign, Project
from .common import Base


class RenkontoEventQuerySet(models.QuerySet):

    def user_events(self, user):
        return self.filter(created_by=user)

    def filter_events(self, filters):
        return self.filter(*filters)

    def to_json(self):
        def event_encoder(field):
            if isinstance(field, datetime):
                return str(field)
            if isinstance(field, models.base.ModelState):
                pass

        result = []
        for event in self:
            result.append(json.dumps(event.__dict__, default=event_encoder))

        return '[{}]'.format(','.join(result))


class RenkontoEvent(Event, Base):

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

    event_type = models.CharField(
        max_length=64
    )

    events = RenkontoEventQuerySet.as_manager()

    @classmethod
    def create(
            cls,
            title, description,
            start_date, start_time, end_date, end_time, all_day,
            calendar, event_type, campaing_name, installation_name
    ):
        self = cls()
        self.title = title
        self.description = description
        self.start = datetime.combine(start_date, start_time or time(0, 0))
        self.end = datetime.combine(end_date, end_time or time(0, 0))
        self.calendar = Calendar.objects.get(id=calendar)
        self.event_type = event_type

        self.campaign = Campaign.objects.get(name=campaing_name)
        self.project = Project.objects.get(name=installation_name)

        self.save()
        return self

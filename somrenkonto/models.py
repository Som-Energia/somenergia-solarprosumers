import json
from datetime import datetime, time

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user
from schedule.models import Calendar, Event

from somsolet.models import Campaign, Project, Engineering
from .common import Base


class EventChoices(object):

    APPOINTMENT = 'APPO'

    UNAVAILABILITY = 'UNAVAIL'

    AVAILABILITY = 'AVAIL'

    choices = [
        (APPOINTMENT, _('Appointment')),
        (UNAVAILABILITY, _('Unavailability')),
        (AVAILABILITY, _('Availability hours'))
    ]


class RenkontoEventQuerySet(models.QuerySet):

    def user_events(self, user):
        return self.filter(created_by=user)

    def filter_events(self, filters):
        return self.filter(*filters)

    def engineering_events(self, engineering_id):
        return self.filter(
            engineering__id=engineering_id
        )

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
        verbose_name=_('Campaign'),
        help_text=_('Campaing of this event')
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('Project'),
        help_text=_('Project of this event')
    )

    engineering = models.ForeignKey(
        Engineering,
        on_delete=models.CASCADE,
        verbose_name=_('Engineering'),
        help_text=_('Engineering related with this event')
    )

    event_type = models.CharField(
        max_length=64,
        choices=EventChoices.choices,
        verbose_name=_('Event type'),
        help_text=_('Type of this event, Appointment, Unavailability or Availability hours')
    )

    all_day = models.BooleanField(
        verbose_name=_('All day'),
        help_text=_('Check if this event will last all day')
    )

    objects = models.Manager()

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
        self.all_day = all_day
        self.calendar = Calendar.objects.get(id=calendar)
        self.event_type = event_type

        self.campaign = Campaign.objects.get(name=campaing_name)
        self.project = Project.objects.get(name=installation_name)
        self.engineering = self.project.engineering

        self.created_by = get_current_authenticated_user()
        self.modified_by = self.created_by

        self.save()
        return self


class CalendarViewChoices(object):
    MONTH_VIEW = 'dayGridMonth'
    
    TIMEGRID_VIEW = 'timeGridWeek'

    LIST_VIEW = 'listWeek'

    DAYGRID_VIEW = 'timeGridDay'

    choices = [
        (_('Month View'), MONTH_VIEW),
        (_('Week View'), TIMEGRID_VIEW),
        (_('Agenda View'), LIST_VIEW),
        (_('Daily View'), DAYGRID_VIEW),
    ]


class CalendarConfig(Base):

    calendar = models.ForeignKey(
        to=Calendar,
        on_delete=models.CASCADE
    )

    default_calendar_view = models.CharField(
        max_length=64,
        choices=CalendarViewChoices.choices,
        default=CalendarViewChoices.MONTH_VIEW,
        verbose_name=_('Default calendar View'),
        help_text=_('What will be the default view of the calendar')
    )


class WeekDays(object):

    MO = 'monday'
    TU = 'tuesday'
    WE = "wednesday"
    TH = 'thursday'
    FR = 'friday'
    SA = 'saturday'
    SU = 'sunday'

    choices = [
        (_('monday'), MO),
        (_('tuesday'), TU),
        (_('wendnesday'), WE),
        (_('thursday'), TH),
        (_('friday'), FR),
        (_('saturday'), SA),
        (_('sunday'), SU),
    ]


class WorkingDay(Base):

    calendar_config = models.ForeignKey(
        to=CalendarConfig,
        on_delete=models.CASCADE,
        related_name='available_days',
        verbose_name=_('Calendar Config'),
        help_text=_('Calendar configuration associated whit this AvailableDay')
    )

    day = models.CharField(
        max_length=64,
        choices=WeekDays.choices,
        verbose_name=_('Day'),
        help_text=_('Calendar configuration associated whit this AvailableDay')
    )

    start = models.TimeField(
        verbose_name=_('Start'),
        help_text=_('At what time starts your work journey')
    )
    
    end = models.TimeField(
        verbose_name=_('End'),
        help_text=_('At what time ends your work journey'),
    )

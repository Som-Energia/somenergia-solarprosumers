import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View
from schedule.models import Calendar

from .models import RenkontoEvent
from .forms import CalendarForm, RenkontoEventForm

logger = logging.getLogger('somrenkonto')


class CalendarView(View):

    def _create_calendar(self, name):
        calendar = Calendar(
            name=name,
            slug=slugify(name)
        )
        calendar.save()
        return calendar

    def _show_calendar_form(self, request):
        context = {
            'calendar_form': CalendarForm()
        }
        return render(request, 'new_calendar.html', context)

    def _show_calendar_view(self, request, calendar):

        event_form = RenkontoEventForm()
        calendar_events = RenkontoEvent.events.all()

        context = {
            'calendar': calendar,
            'event_form': event_form,
            'calendar_events': calendar_events.to_json()
        }
        return render(request, 'calendar.html', context)

    def get(self, request):
        try:
            ing_calendar = Calendar.objects.get_calendar_for_object(request.user)
        except Calendar.DoesNotExist:
            return self._show_calendar_form(request)

        return self._show_calendar_view(
            request,
            calendar=ing_calendar
        )

    def post(self, request):
        calendar_form = CalendarForm(request.POST)
        if calendar_form.is_valid():
            calendar = self._create_calendar(**calendar_form.cleaned_data)
            calendar.create_relation(request.user)

        return HttpResponseRedirect(reverse('somrenkonto'))


class SomRenkontoEventView(View):

    def post(self, request):
        event_form = RenkontoEventForm(request.POST)
        if event_form.is_valid():
            renkonto_event = RenkontoEvent.create(**event_form.cleaned_data)
            logger.debug(renkonto_event.__dict__)

        return HttpResponseRedirect(reverse('somrenkonto'))

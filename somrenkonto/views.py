import json
import logging

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View
from schedule.models import Calendar
from somsolet.models import Campaign, Engineering, Project

from .forms import CalendarForm, CalendarConfigForm, RenkontoEventForm
from .models import RenkontoEvent, CalendarConfig

logger = logging.getLogger('somrenkonto')


class FilterViewMixin(object):

    def get_filter_params(self, request):
        query_dict = request.GET.copy()
        filter_queries = []

        params = {
            field: [type_(value) for value in query_dict.get(field).split(',')]
                for field, type_ in self.FILTER_FIELDS if field in query_dict
        }
        for field, value in params.items():
            if len(value) == 1:
                filter_queries.append(Q(**{field: value[0]}))
            else:
                filter_queries.append(Q(**{f'{field}__in': value}))

        return filter_queries


class CalendarView(FilterViewMixin, View):

    FILTER_FIELDS = [
        ('campaign_id', int),
        ('project_id', int),
        ('event_type', str)
    ]

    def _get_campaigns(self, request):
        campaigns = Campaign.campaigns.user_campaigns(request.user)
        return {
            campaign.name: {
                'id': campaign.id,
                'installations': list(Project.objects.filter(campaign=campaign).values('name', 'id'))
            }
            for campaign in campaigns
        }

    def _get_calendar_events(self, request):
        filters = self.get_filter_params(request)
        filters.append(
            Q(campaign__in=Campaign.campaigns.user_campaigns(request.user))
        )
        return RenkontoEvent.events.filter_events(filters)

    def _create_calendar(self, name):
        calendar = Calendar(
            name=name,
            slug=slugify(name)
        )
        calendar.save()
        CalendarConfig.objects.get_or_create(
            calendar=calendar
        )
        return calendar

    def _show_calendar_form(self, request, template):
        context = {
            'calendar_form': CalendarForm()
        }
        return render(request, template, context)

    def _show_calendar_view(self, request, calendar, template):
        event_form = RenkontoEventForm()
        calendar_events = self._get_calendar_events(request)
        campaigns = self._get_campaigns(request)

        context = {
            'calendar': calendar,
            'event_form': event_form,
            'calendar_events': calendar_events.to_json(),
            'campaigns': json.dumps(campaigns)
        }
        return render(request, template, context)

    def get(self, request):
        try:
            ing_calendar = Calendar.objects.get_calendar_for_object(request.user)
        except Calendar.DoesNotExist:
            return self._show_calendar_form(request, 'new_calendar.html')
        else:
            return self._show_calendar_view(
                request,
                calendar=ing_calendar,
                template='calendar.html'
            )

    @transaction.atomic()
    def post(self, request):
        calendar_form = CalendarForm(request.POST)
        if calendar_form.is_valid():
            calendar = self._create_calendar(**calendar_form.cleaned_data)
            calendar.create_relation(request.user)

        return HttpResponseRedirect(reverse('somrenkonto'))


class EditCalendarView(View):
    def get(self, request, pk):
        context = {
            'calendar_config': CalendarConfig.objects.get(calendar__id=pk),
            'config_form': CalendarConfigForm()
        }
        return render(request, 'edit_calendar.html', context=context)


class SomRenkontoEventView(View):

    def _get_url_to_go(self, request, view_name):
        return request.META.get('HTTP_REFERER') or reverse(view_name)

    def post(self, request):
        event_form = RenkontoEventForm(request.POST)
        if event_form.is_valid():
            renkonto_event = RenkontoEvent.create(**event_form.cleaned_data)

        url_to_go = self._get_url_to_go(request, 'somrenkonto')
        return HttpResponseRedirect(url_to_go)

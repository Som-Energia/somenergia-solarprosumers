import pytest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import Client
from django.urls import reverse

from .models import RenkontoEvent
from .views import CalendarView, EditCalendarView, FilterViewMixin

client = Client()


@pytest.mark.django_db
class TestFilterViewMixin:

    FILTER_FIELDS = [
        ('campaign_id', int),
        ('project_id', int),
        ('event_type', str)
    ]

    def test__get_filter_params__single_value(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1&project_id=2'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == [Q(campaign_id=1), Q(project_id=2)]

    def test__get_filter_params__multiple_value(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1,2&project_id=5,6'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == [
            Q(campaign_id__in=[1,2]), Q(project_id__in=[5,6])
        ]

    def test__get_filter_params__single_value_string_type(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1&event_type=APPO'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == [Q(campaign_id=1), Q(event_type='APPO')]

    def test__get_filter_params__multiple_value_srting_type(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1,2&event_type=APPO,UNAVAIL'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == [
            Q(campaign_id__in=[1,2]), Q(event_type__in=['APPO', 'UNAVAIL'])
        ]


@pytest.mark.django_db
class TestCalendarView:

    def test__edit_calendar_conf(self, rf, calendar_with_conf):
        # given a calendar
        # calendar_with_conf

        # when we access to its configuration
        url = reverse('edit_calendar', kwargs={'pk': calendar_with_conf.id})
        request = rf.get(url)
        response = EditCalendarView.as_view()(request, pk=calendar_with_conf.id)

        # then we obtain a successful response
        assert response.status_code == 200

    def test__edit_calendar_conf__button_in_calendar_view(
            self, rf, calendar, engineering_user_paco
    ):
        # given a calendar
        # calendar
        # and a user
        # user

        # when that user visit that calendar
        url = reverse('somrenkonto')
        request = rf.get(url)
        request.user = engineering_user_paco
        response = CalendarView.as_view()(request)
        # and check for the calendar button configuration
        conf_calendar_url = reverse(
            'edit_calendar', kwargs={'pk': calendar.id}
        )

        # then the url to go to the configuration is in the button
        assert conf_calendar_url in response.content.decode()


@pytest.mark.django_db
class TestRenkontoEventQuerySet:

    def test__technical_visit(self, technical_visit_event):
        # Given a project and technical visit event for that project
        # technical_visit_event
        # technical_visit_event.project

        # when we search for all technical visits
        events = RenkontoEvent.events.technical_visit(technical_visit_event.project)

        # then we obtain the same event
        assert events.count() == 1
        assert events.first() == technical_visit_event

    def test__engineering_events(self, engineering_with_events):
        # given
        # an engineering with calendar events
        engineering_id = engineering_with_events.id

        # when we search all events by engineering id
        events = RenkontoEvent.events.engineering_events(engineering_id)

       # then we have a list of that events
        assert len(events) > 0
        assert list(events) == list(RenkontoEvent.objects.filter(
            engineering__id=engineering_id
        ))

    def test__engineering_without_events(
            self, engineering_without_events, engineering_with_events
    ):
        # given
        # an engineering without events and other engineering with events

        # when we search all events of the engineering without events
        events = RenkontoEvent.events.engineering_events(engineering_without_events.id)

        # then we haven't events
        assert len(events) == 0

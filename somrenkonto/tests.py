import pytest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import Client
from django.urls import reverse

from somsolet.models import Engineering
from . import factories
from .models import RenkontoEvent
from .views import CalendarView, EditCalendarView, FilterViewMixin

client = Client()


@pytest.mark.skip
@pytest.mark.django_db
def test__calendar_view(rf):
    User = get_user_model()
    url = reverse('somrenkonto')
    request = rf.get(url)
    request.user = User.objects.first()

    response = CalendarView.as_view()(request)

    assert 'Obras' in response.content.decode()


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
   
    def test__edit_calendar_conf(self, rf):
       calendar_conf_id = 1
       url = reverse('edit_calendar', kwargs={'pk': calendar_conf_id})
       request = rf.get(url)

       response = EditCalendarView.as_view()(request, pk=calendar_conf_id)

       assert response.status_code == 200
    
    @pytest.mark.skip
    def test__edit_calendar_conf__button_in_calendar_view(self, rf):
        User = get_user_model()
        url = reverse('somrenkonto')
        calendar_conf_id = 1
        request = rf.get(url)
        request.user = User.objects.first()
        
        response = CalendarView.as_view()(request)
        conf_calendar_url = reverse('edit_calendar', kwargs={'pk': calendar_conf_id})

        assert conf_calendar_url in response.content.decode()


@pytest.mark.django_db
class TestRenkontoEventQuerySet:

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

    def test__engineering_without_events(self, engineering, engineering_with_events):
        # given
        # an engineering without events and other engineering with events

        # when we search all events of the engineering without events
        events = RenkontoEvent.events.engineering_events(engineering.id)

        # then we haven't events
        assert len(events) == 0

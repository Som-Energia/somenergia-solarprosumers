import pytest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import Client
from django.urls import reverse

from . import factories
from .views import CalendarView, FilterViewMixin

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

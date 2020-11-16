import pytest
from django.contrib.auth import get_user_model
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

    def test__get_filter_params(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == {'campaign_id': [1]}

    def test__get_filter_params(self, rf):
        base_url = reverse('somrenkonto')
        url = f'{base_url}?campaign_id=1,2'
        request = rf.get(url)

        filter_view_mixin = FilterViewMixin()
        filter_view_mixin.FILTER_FIELDS = self.FILTER_FIELDS

        filter_params = filter_view_mixin.get_filter_params(request)

        assert filter_params == {'campaign_id': [1]}

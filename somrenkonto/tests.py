from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
import pytest

from .views import CalendarView
from . import factories

client = Client()

@pytest.mark.django_db
def test__calendar_view(rf, ):
    User = get_user_model()
    url = reverse('somrenkonto')
    request = rf.get(url)
    request.user = User.objects.first()

    response = CalendarView.as_view()(request)

    assert 'Obras' in response.content.decode()

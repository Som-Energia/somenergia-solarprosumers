from django.test import Client
from django.urls import reverse
import pytest

from .views import CalendarView


client = Client()

def test__calendar_view(client):
    url = reverse('somrenkonto')
    response = client.get(url)

    assert 'hola' in response.content.decode()

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import Client
from django.urls import reverse

from somsolet.models import Engineering
from . import factories
from .models import RenkontoEvent
from .views import CalendarView, EditCalendarView, FilterViewMixin


@pytest.mark.django_db
class TestProjectModel:

    def test__technical_visit_dates(self, technical_visit_event):
        # Given a project and technical visit event for that project
        # technical_visit_event.project
        # technical_visit_event
        project = technical_visit_event.project

        # when we look for that date in project
        technical_visit_dates = project.technical_visit_dates()

        # then we have that technical visit event
        assert technical_visit_dates.count() == 1
        assert technical_visit_dates.first() == technical_visit_event





import pytest

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from somsolet.models import (Campaign, Project)
from somrenkonto.models import RenkontoEvent
from somsolet_api.views import RenkontoEventView
from somsolet_api.serializer import RenkontoEventSerializer

from .factories import TechnicalVisitDataFactory
from somsolet.tests.fixtures import ProjectFactory
from somsolet.tests.factories import SuperuserFactory
from somrenkonto.factories import CalendarConfigMonthViewFactory


class TestAPI(TestCase):

    def setUp(self):
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_auth(self):
        login_response = self.client.login(
            username=self.user.username, password='1234'
        )
        assert login_response == True


class TestStages(TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/stages/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_stages_base_case(self):
        self.client.login(username=self.user.username, password='1234')

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list

    def test_stages_user_unauthenticated(self):
        response = self.client.get(self.base_url)

        assert response.status_code == 401


class TestCampaign(TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/campaign/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()
        # TODO: Create a test Campaign

    def tearDown(self):
        self.user.delete()

    def test_campaign_user_unauthenticated_permitted(self):
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert response.json() == []

    def test_campaign_user_unauthenticated_post(self):
        response = self.client.post(self.base_url, {})

        assert response.status_code == 401

    def test_campaign_authenticated_user(self):
        self.client.login(username=self.user.username, password='1234')

        response = self.client.get(self.base_url)

        assert response.status_code == 200

    def test_campaign_user_permitted(self):
        self.client.login(username=self.user.username, password='1234')
        permission = Permission.objects.get(codename='view_campaign')
        self.user.user_permissions.add(permission)

        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert response.json() == []


class TestProject(TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/project/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()
        # TODO: Create a test Project

    def tearDown(self):
        self.user.delete()

    def test_project_user_unauthenticated(self):
        response = self.client.get(self.base_url)

        assert response.status_code == 401

    def test_project_user_not_permitted(self):
        self.client.login(username=self.user.username, password='1234')

        response = self.client.get(self.base_url)

        assert response.status_code == 403

    def test_project_user_permitted(self):
        self.client.login(username=self.user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        self.user.user_permissions.add(permission)

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body == []

    def test_set_technical_visit(self):
        # given
        # a technical visit, an admin, a calendar and a project
        technical_visit = TechnicalVisitDataFactory.data_ok()
        admin_user = user = SuperuserFactory.create()
        calendar = CalendarConfigMonthViewFactory.create()
        montse_project = ProjectFactory.create()
        calendar.calendar.create_relation(montse_project.engineering.user)

        # with an engineering with permissions
        self.client.login(username=admin_user.username, password='1234')

        # when we set a technical visit for a project
        url = '{base_url}{id}/set_technical_visit/'.format(
            base_url=self.base_url, id=montse_project.id
        )
        response = self.client.put(url, data=technical_visit, content_type='application/json')

        # then everything is ok
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == {
            'dateStart': technical_visit.get('date_start'),
            'dateEnd': technical_visit.get('date_end'),
            'allDay': False,
            'eventType': 'TECH',
            'address': None,
            'installationId': montse_project.id,
            'campaignId': montse_project.campaign_id
        }


class TestEvents:

    @pytest.mark.django_db
    def test_get_engineering_events(
        self, authenticated_user, engineering_with_events, client, rf
    ):
        # given
        # an authenticated_user
        # an engineering with events

        # when the user requests for the events of an engineering
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.get(url)
        request.user = authenticated_user
        client.login(username=authenticated_user.username, password='1234')
        response = client.get(url)

        # then the user obtain a succesfull response and a list with the events of the engineering
        assert response.status_code == 200
        events = [
            RenkontoEventSerializer(event, context={'request': request}).data
            for event in RenkontoEvent.objects.filter(
                engineering__id=engineering_with_events.id
            )
        ]
        assert response.data == {
            'state': True,
            'data': {
                'count': len(events),
                'results': events
            }
        }


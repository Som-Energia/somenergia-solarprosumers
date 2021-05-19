import pytest

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from somsolet.models import (Campaign, Project)
from somrenkonto.models import RenkontoEvent
from somsolet_api.views import RenkontoEventView
from somsolet_api.serializer import RenkontoEventSerializer


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


class TestEvents:

    @pytest.mark.django_db
    def test_get_engineering_events(
        self, authenticated_user, engineering_with_events, client,
    ):
        # given
        # an authenticated_user
        # an engineering with events

        # when the user requests for the events of an engineering
        url = reverse('events', args=[engineering_with_events.id])
        client.login(username=authenticated_user.username, password='1234')
        response = client.get(url)

        # then the user obtain a succesfull response and a list with the events of the engineering
        assert response.status_code == 200
        events = [
            RenkontoEventSerializer(event).data
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


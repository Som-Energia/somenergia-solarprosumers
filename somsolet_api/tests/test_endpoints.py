from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import resolve, reverse

from somsolet.models import (Campaign, Project)


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

        assert response.status_code == 403


class TestCampaign(TestCase):
    
    def setUp(self):
        self.base_url = '/somsolet-api/campaign/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()
        # TODO: Create a test Campaign

    def tearDown(self):
        self.user.delete()

    def test_campaign_user_unauthenticated(self):
        response = self.client.get(self.base_url)

        assert response.status_code == 403

    def test_campaign_user_not_permitted(self):
        self.client.login(username=self.user.username, password='1234')

        response = self.client.get(self.base_url)

        assert response.status_code == 403

    def test_campaign_user_permitted(self):
        self.client.login(username=self.user.username, password='1234')
        permission = Permission.objects.get(codename='view_campaign')
        self.user.user_permissions.add(permission)

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body == []

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

        assert response.status_code == 403

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

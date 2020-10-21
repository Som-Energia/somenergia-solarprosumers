from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from somsolet.models import (Campaign, Project)


class TestStages(TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/stages/'
        self.user = User(username='aitor', password='1234')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_stages_base_case(self):
        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list


class TestCampaign(TestCase):
    
    def setUp(self):
        self.base_url = '/somsolet-api/campaign/'
        self.user = User(username='aitor', password='1234')
        self.user.save()
        # TODO: Create a test Campaign

    def tearDown(self):
        self.user.delete()

    def test_stages_base_case(self):
        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body == []


class TestProject(TestCase):
    
    def setUp(self):
        self.base_url = '/somsolet-api/project/'
        self.user = User(username='aitor', password='1234')
        self.user.save()
        # TODO: Create a test Project

    def tearDown(self):
        self.user.delete()

    def test_project_base_case(self):
        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body == []

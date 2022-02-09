import jwt
import pytest

from django.contrib.auth.models import User, Permission
from django_currentuser.middleware import _set_current_user
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication

from somsolet.models import (Campaign, Project)
from somrenkonto.models import RenkontoEvent
from somsolet_api.views import RenkontoEventView
from somsolet_api.serializer import RenkontoEventSerializer

from .factories import TechnicalVisitDataFactory
from somrenkonto.factories import CalendarConfigMonthViewFactory
from somsolet_api.tests.common import LoginMixin

#from somsolet.tests.fixtures import ProjectFactory
from somsolet.tests.factories import (CampaignFactory, ClientFactory, EngineeringFactory,
                        ProjectFactory, TechnicalDetailsFactory, UserFactory, LocalGroupFactory, SuperuserFactory)



class TestAPI(LoginMixin, APITestCase):

    def setUp(self):
        self.user = User(
            username='aitor',
            first_name='Aitor',
            last_name='Menta',
            email='aitor.menta@somenergia.coop',
            password='1234'
        )
        self.user.set_password('1234')
        self.user.save()
        self.client = APIClient()

        self.login(self.user)

    def tearDown(self):
        self.user.delete()

    # client is APIClient
    def test_session_auth(self):
        login_response = self.client.login(
            username=self.user.username, password='1234'
        )
        assert login_response == True

    def test_simple_request(self):
        base_url = '/somsolet-api/stages/'

        response = self.client.get(base_url)
        assert response.status_code == 200

    def test_jwt_content(self):
        login_resp = self.client.post(
            reverse('token_obtain_pair'),
            data={"username": 'aitor', "password": '1234'},
            format='json'
        )
        token = login_resp.json().get('access')

        payload = jwt.decode(token, options={"verify_signature": False})

        assert payload.get('name', 'JWT content not found') == self.user.get_full_name()
        assert payload.get('email', 'JWT content not found') == self.user.email
        assert payload.get('username', 'JWT content not found') == self.user.get_username()

    # TODO replace claims to attempt to perform identity theft, it's not a joke, jim
    def test_jwt_attack(self):

        login_resp = self.client.post(reverse('token_obtain_pair'), data={"username": 'aitor', "password": '1234'}, format='json')

        login_resp = self.client.post(
            reverse('token_obtain_pair'),
            data={"username": 'aitor', "password": '1234'},
            format='json'
        )
        token = login_resp.json().get('access')

        payload = jwt.decode(token, options={"verify_signature": False})
        payload['user_id'] = 2
        payload['username'] = 'Tilla'
        bad_token = jwt.encode(payload, key='lalatra', algorithm="HS256")
        header, code_payload, _ = bad_token.split('.')
        new_token = "{}.{}.{}".format(
            header, code_payload, token.split('.')[-1]
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='{} {}'.format(
                'Bearer',
                new_token
            )
        )

        base_url = '/somsolet-api/stages/'
        response = self.client.get(base_url)

        assert response.status_code == 401

    # TODO test a simple request
    def _test_simple_request_with_APIRequestFactory(self):
        # TODO use APIRequestFactory and force_authenticate
        pass

class TestStages(LoginMixin, TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/stages/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()

        self.client = APIClient()
        project = ProjectFactory.create()

    def tearDown(self):
        self.user.delete()

    def test_stages_user_unauthenticated(self):
        response = self.client.get(self.base_url)

        assert response.status_code == 401

    def test_stages_base_case(self):
        login_resp = self.client.post(
            reverse('token_obtain_pair'),
            data={"username": "aitor", "password": '1234'},
            format='json'
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='{} {}'.format(
                'Bearer',
                login_resp.json().get('access', '')
            )
        )

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list

    def test_stages_prereport_own_case(self):

        self.base_url = '/somsolet-api/prereport/'

        # permission = Permission.objects.get(codename='view_prereportstage')
        # self.user.user_permissions.add(permission)

        permission = Permission.objects.get(codename='view_project')
        self.user.user_permissions.add(permission)

        # for p in Permission.objects.all():
        #     self.user.user_permissions.add(p)

        self.login(self.user) # i afegir LoginMixin a la class

        # login_resp = self.client.post(
        #     reverse('token_obtain_pair'),
        #     data={"username": "N8215601I", "password": '1234'},
        #     format='json'
        # )
        # self.client.credentials(
        #     HTTP_AUTHORIZATION='{} {}'.format(
        #         'Bearer',
        #         login_resp.json().get('access', '')
        #     )
        # )

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list

    def test_stages_prereport_other_s_case(self):

        self.base_url = '/somsolet-api/prereport/'

        login_resp = self.client.post(
            reverse('token_obtain_pair'),
            data={"username": "aitor", "password": '1234'},
            format='json'
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='{} {}'.format(
                'Bearer',
                login_resp.json().get('access', '')
            )
        )

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list

    def test_stages_prereport_admin_case(self):

        self.base_url = '/somsolet-api/prereport/'
        self.user.is_staff = True
        self.user.save()

        login_resp = self.client.post(
            reverse('token_obtain_pair'),
            data={"username": "aitor", "password": '1234'},
            format='json'
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='{} {}'.format(
                'Bearer',
                login_resp.json().get('access', '')
            )
        )

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body.__class__ is list




class TestCampaign(TestCase):

    def setUp(self):
        self.base_url = '/somsolet-api/campaign/'
        self.user = User(username='aitor', password='1234')
        self.user.set_password('1234')
        self.user.save()
        # TODO: Create a test Campaign
        campaign = CampaignFactory.create()

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


class TestProject(LoginMixin, APITestCase):

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
        self.login(self.user)

        response = self.client.get(self.base_url)

        assert response.status_code == 403

    def test_project_user_permitted(self):
        self.login(self.user)
        permission = Permission.objects.get(codename='view_project')
        self.user.user_permissions.add(permission)

        response = self.client.get(self.base_url)

        response_body = response.json()
        assert response.status_code == 200
        assert response_body == []

    def test_set_technical_visit(self):
        # given
        # an admin user, a calendar, a technical visit, and a project
        admin_user = SuperuserFactory.create()
        _set_current_user(admin_user)
        calendar = CalendarConfigMonthViewFactory.create()
        technical_visit = TechnicalVisitDataFactory.data_ok()
        montse_project = ProjectFactory.create()
        calendar.calendar.create_relation(montse_project.engineering.user)

        # with an engineering with permissions
        self.login(admin_user)

        # when we set a technical visit for a project
        url = '{base_url}{id}/set_technical_visit/'.format(
            base_url=self.base_url, id=montse_project.id
        )
        response = self.client.put(url, data=technical_visit, format='json')

        # then everything is ok
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == {
            'dateStart': technical_visit.get('date_start'),
            'dateEnd': technical_visit.get('date_end'),
            'allDay': False,
            'eventType': 'TECH',
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


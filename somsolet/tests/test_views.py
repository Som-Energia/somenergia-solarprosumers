from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from parameterized import parameterized

from somsolet.views import (PrereportView, ProjectView, TechnicalVisitView,
                            ReportView, OfferView, SignatureView,
                            ConstructionPermitView, InstallationDateView,
                            DeliveryCertificateView, LegalRegistrationView,
                            LegalizationView)

from .factories import ProjectFactory, UserFactory

from .conftest import campaing__solar_paco, technical_details

def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        param.args[0].__name__,
    )


class TestHomeView:
    
    def test__engineering_home_view(self):
        path = reverse('home')
        request = RequestFactory().get(path)
        request.user = UserFactory()


@pytest.mark.django_db
class TestViews:

    def get_initial_mock(self, status='random'):
        project = ProjectFactory.build()

        return {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': status,
            'campaign_pk': 123  # random
        }

    @pytest.mark.skip(reason="WIP: must use mock")
    def test_project_detail_authenticated(self):
        path = reverse('project', kwargs={'pk': 2})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = ProjectView.as_view()(request, pk=2)
        assert response.status_code == 200

    @pytest.mark.skip(reason="WIP: must use mock")
    def test_project_detail_unauthenticated(self):
        path = reverse('project', kwargs={'pk': 2})
        request = RequestFactory().get(path)
        reqauest.user = AnonymousUser()

        response = ProjectView.as_view()(request, pk=2)
        assert 'auth/login' in response.url

    @parameterized.expand(
        [
            [PrereportView, 'prereport', 'data downloaded'],
            [TechnicalVisitView, 'technical_visit', 'technical visit'],
            [ReportView, 'report', 'report'],
            [OfferView, 'offer', 'report'],
            [SignatureView, 'signed_contract', 'signature'],
            [ConstructionPermitView, 'construction_permit', 'construction permit'],
            [InstallationDateView, 'installation_date', 'date installation set'],
            [DeliveryCertificateView, 'delivery_certificate', 'end installation'],
            [LegalRegistrationView, 'legal_registration', 'end installation'],
            [LegalizationView, 'legalization', 'legalization']
        ], name_func=custom_name_func
    )
    def test_auth_valid_status_condition(self, view, url_name, status):
        with patch.object(
            view,
            'get_initial',
            return_value=self.get_initial_mock(status)
        ):
            path = reverse(url_name, kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = view.as_view()(request, pk=1)
            assert response.status_code == 200

    @parameterized.expand(
        [
            [PrereportView, 'prereport'],
            [TechnicalVisitView, 'technical_visit'],
            [ReportView, 'report'],
            [OfferView, 'offer'],
            [SignatureView, 'signed_contract'],
            [ConstructionPermitView, 'construction_permit'],
            [InstallationDateView, 'installation_date'],
            [DeliveryCertificateView, 'delivery_certificate'],
            [LegalRegistrationView, 'legal_registration'],
            [LegalizationView, 'legalization']
        ], name_func=custom_name_func
    )
    def test_auth_invalid_status_condition(self, view, url_name):
        with patch.object(
            view,
            'get_initial',
            return_value=self.get_initial_mock()
        ):
            path = reverse(url_name, kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = view.as_view()(request, pk=1)
            assert 'project' in response.url

    @parameterized.expand(
        [
            [PrereportView, 'prereport'],
            [TechnicalVisitView, 'technical_visit'],
            [ReportView, 'report'],
            [OfferView, 'offer'],
            [SignatureView, 'signed_contract'],
            [ConstructionPermitView, 'construction_permit'],
            [InstallationDateView, 'installation_date'],
            [DeliveryCertificateView, 'delivery_certificate'],
            [LegalRegistrationView, 'legal_registration'],
            [LegalizationView, 'legalization']
        ], name_func=custom_name_func
    )
    def test_unauthenticated(self, view, url_name):
        with patch.object(
            view,
            'get_initial',
            return_value=self.get_initial_mock()
        ):
            path = reverse(url_name, kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = view.as_view()(request, pk=1)
            assert 'auth/login' in response.url

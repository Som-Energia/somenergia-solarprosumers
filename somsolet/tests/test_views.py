from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from parameterized import parameterized

from somsolet.views import (CampaignSetView, ConstructionPermitView,
                            DeliveryCertificateView, InstallationDateView,
                            LegalizationView, LegalRegistrationView, OfferView,
                            PrereportView, ProjectView, ReportView,
                            SignatureView, TechnicalVisitView)

from .factories import ProjectFactory, UserFactory
from .fixtures import (campaing__solar_paco, client, engenieering,
                       engenieering_user, project, technical_details)


def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        param.args[0].__name__,
    )


@pytest.mark.django_db
class TestHomeView:

    def test__engineering_home_view__whitout_campaings(
            self,
            rf,
            engenieering_user, engenieering
    ):
        engenieering.user = engenieering_user
        path = reverse('home')
        request = rf.get(path)
        request.user = engenieering_user

        response = CampaignSetView.as_view()(request)

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Campaign' in content and \
            'Active' in content and \
            'Technical Details' in content and \
            'Calendar' in content


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

    def test_project_detail_authenticated(
            self,
            rf,
            project, engenieering_user, campaing__solar_paco, client
    ):
        path = reverse('project', kwargs={'pk': project.pk})
        request = rf.get(path)
        request.user = engenieering_user

        response = ProjectView.as_view()(request, pk=project.pk)
        assert response.status_code == 200

    @pytest.mark.skip(reason="WIP: must use mock")
    def test_project_detail_unauthenticated(self):
        path = reverse('project', kwargs={'pk': 2})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

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
            # request.user = mixer.blend(User)

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
            # request.user = mixer.blend(User)

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

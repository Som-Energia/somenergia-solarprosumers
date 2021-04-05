from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from somsolet.views import (CampaignSetView, ConstructionPermitView,
                            DeliveryCertificateView, InstallationDateView,
                            LegalizationView, LegalRegistrationView, OfferView,
                            PrereportView, ProjectView, ReportView,
                            SignatureView, TechnicalVisitView)

from .factories import (CampaignFactory, ClientFactory, EngineeringFactory,
                        ProjectFactory, TechnicalDetailsFactory, UserFactory, LocalGroupFactory)
from .fixtures import *


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
            engineering_user, engineering
    ):
        engineering.user = engineering_user
        path = reverse('home')
        request = rf.get(path)
        request.user = engineering_user

        response = CampaignSetView.as_view()(request)

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Campaign' in content and \
            'Active' in content and \
            'Technical Details' in content and \
            'Calendar' in content


@pytest.mark.django_db()
class TestViews:

    def test_project_detail_authenticated(
        self, rf, project, engineering_user
    ):
        path = reverse('project', kwargs={'pk': project.pk})
        request = rf.get(path)
        request.user = engineering_user

        response = ProjectView.as_view()(request, pk=project.pk)
        assert response.status_code == 200


    def test_project_detail_unauthenticated(
        self, rf, project
    ):
        path = reverse('project', kwargs={'pk': project.pk})
        request = rf.get(path)
        request.user = AnonymousUser()

        response = ProjectView.as_view()(request, pk=project.pk)
        assert 'auth/login' in response.url

    @pytest.mark.parametrize("view,url_name,status",
        [
            [PrereportView, 'prereport', 'registered']
        ]
    )
    def test_auth_prereport_status_condition(
        self, view, url_name, status
    ):
        project = ProjectFactory()
        path = reverse(url_name, kwargs={'pk': project.pk})
        request = RequestFactory().get(path)
        request.user = UserFactory()

        response = view.as_view()(request, pk=project.pk)
        assert response.status_code == 200

    @pytest.mark.parametrize("view,url_name,status",
        [
            [TechnicalVisitView, 'technical_visit', 'technical visit'],
            [ReportView, 'report', 'report'],
            [OfferView, 'offer', 'report'],
            [SignatureView, 'signed_contract', 'signature'],
            [ConstructionPermitView, 'construction_permit', 'construction permit'],
            [InstallationDateView, 'installation_date', 'date installation set'],
            [DeliveryCertificateView, 'delivery_certificate', 'end installation'],
            [LegalRegistrationView, 'legal_registration', 'end installation'],
            [LegalizationView, 'legalization', 'legalization']
        ]
    )
    def test_auth_redirect_whith_invalid_status_condition(
        self, view, url_name, status        
    ):
        project = ProjectFactory()
        path = reverse(url_name, kwargs={'pk': project.pk})
        request = RequestFactory().get(path)
        request.user = UserFactory()

        response = view.as_view()(request, pk=project.pk)
        assert response.status_code == 302

    @pytest.mark.parametrize("view,url_name",
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
        ]
    )
    def test_unauthenticated(self, view, url_name):
        project = ProjectFactory()
        path = reverse(url_name, kwargs={'pk': project.pk})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = view.as_view()(request, pk=project.pk)
        assert 'auth/login' in response.url

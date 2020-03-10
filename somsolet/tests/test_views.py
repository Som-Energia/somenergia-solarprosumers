
import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from factories import ProjectFactory
from mixer.backend.django import mixer
from mock import patch
from somsolet.views import (PrereportView, ProjectView, TechnicalVisitView,
                            ReportView, OfferView, SignatureView,
                            ConstructionPermitView, InstallationDateView,
                            DeliveryCertificateView, LegalizationView)


@pytest.mark.django_db
class TestViews:

    @pytest.mark.skip(reason="WIP: must use mock")
    def test_project_detail_authenticated(self):
        path = reverse('project', kwargs={'pk': 2})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = ProjectView.as_view()(request, pk=2)
        assert response.status_code == 200

    def test_project_detail_unauthenticated(self):
        path = reverse('project', kwargs={'pk': 2})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = ProjectView.as_view()(request, pk=2)
        assert 'auth/login' in response.url

    def test_prereport_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'data downloaded'
        }
        with patch.object(
            PrereportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('prereport', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = PrereportView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_prereport_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            PrereportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('prereport', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = PrereportView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_prereport_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            PrereportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('prereport', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = PrereportView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_technical_visit_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'technical visit'
        }
        with patch.object(
            TechnicalVisitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = TechnicalVisitView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_technical_visit_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            TechnicalVisitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = TechnicalVisitView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_technical_visit_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            TechnicalVisitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = TechnicalVisitView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_report_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'report'
        }
        with patch.object(
            ReportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = ReportView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_report_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            ReportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = ReportView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_report_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            ReportView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = ReportView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_offer_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'report'
        }
        with patch.object(
            OfferView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = OfferView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_offer_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            OfferView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = OfferView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_offer_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            OfferView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = OfferView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_signature_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'signature'
        }
        with patch.object(
            SignatureView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = SignatureView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_signature_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            SignatureView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = SignatureView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_signature_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            SignatureView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = SignatureView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_construction_permit_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'construction permit'
        }
        with patch.object(
            ConstructionPermitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = ConstructionPermitView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_construction_permit_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            ConstructionPermitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = ConstructionPermitView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_construction_permit_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            ConstructionPermitView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = ConstructionPermitView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_installation_date_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'construction permit'
        }
        with patch.object(
            InstallationDateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = InstallationDateView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_installation_date_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            InstallationDateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = InstallationDateView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_installation_date_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            InstallationDateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = InstallationDateView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_delivery_cert_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'end installation'
        }
        with patch.object(
            DeliveryCertificateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = DeliveryCertificateView.as_view()(request, pk=1)
            assert response.status_code == 200

    def test_delivery_cert_auth_invalid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            DeliveryCertificateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = DeliveryCertificateView.as_view()(request, pk=1)
            assert 'project' in response.url

    def test_delivery_cert_unauthenticated(self):
        project = ProjectFactory.build()
        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'random',
            'campaign_pk': 2
        }
        with patch.object(
            DeliveryCertificateView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = AnonymousUser()

            response = DeliveryCertificateView.as_view()(request, pk=1)
            assert 'auth/login' in response.url

    def test_legalization_auth_valid_status_condition(self):
        project = ProjectFactory.build()

        get_initial_mock = {
            'campaign': project.campaign,
            'project': project.id,
            'client': project.client,
            'status': 'legalization'
        }
        with patch.object(
            LegalizationView,
            'get_initial',
            return_value=get_initial_mock
        ):
            path = reverse('technical_visit', kwargs={'pk': 1})
            request = RequestFactory().get(path)
            request.user = mixer.blend(User)

            response = LegalizationView.as_view()(request, pk=1)
            assert response.status_code == 200

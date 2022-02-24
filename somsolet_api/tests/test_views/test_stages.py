import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APITestCase
from somsolet_api.tests.common import LoginMixin

from somsolet.tests.factories import (ProjectDeliveryCertificateStageFactory,
                                      ProjectEmptyStatusStageFactory,
                                      ProjectFactory,
                                      ProjectLegalizationStageFactory,
                                      ProjectLegalRegistrationStageFactory,
                                      ProjectOfferStageFactory,
                                      ProjectOfferAcceptedStageFactory,
                                      ProjectPermitStageFactory,
                                      ProjectPrereportRegisteredStageFactory,
                                      ProjectPrereportStageFactory,
                                      ProjectSecondInvoiceStageFactory,
                                      ProjectSignatureStageFactory,
                                    )


class TestPrereportViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)

        super().login(user)
        return user

    @pytest.mark.django_db
    def test_prereport_patch__base_case(self):
        project = ProjectPrereportRegisteredStageFactory()

        assert project.prereport.check is False
        assert project.status == 'registered'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': False},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidPrereport'] is False
        assert project.status == 'prereport'

    @pytest.mark.django_db
    def test_prereport_patch__review_status(self):
        project = ProjectPrereportStageFactory()

        assert project.status == 'prereport'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidPrereport'] is True
        assert project.status == 'prereport review'

    @pytest.mark.django_db
    def test_prereport_patch__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()
        assert project.prereport.check is False
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'

    @pytest.mark.django_db
    def test_prereport_put__base_case(self):
        project = ProjectPrereportRegisteredStageFactory()

        assert project.prereport.upload.name is None
        assert project.status == 'registered'

        user = self.login(project.engineering.user)

        prereport_image = SimpleUploadedFile(
            name='prereport.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/prereport/?projectId=1',
            data={'upload': prereport_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'prereport'

    @pytest.mark.django_db
    def test_prereport_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.prereport.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        prereport_image = SimpleUploadedFile(
            name='prereport.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/prereport/?projectId=1',
            data={'upload': prereport_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestReportViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_report_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'prereport'
        project.save()

        assert project.report.check is False
        assert project.status == 'prereport'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/report/?projectId=1',
            data={'is_checked': False},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidReport'] is False
        assert project.status == 'report'
    
    @pytest.mark.django_db
    def test_report_patch__review_status(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'report'
        project.save()

        assert project.status == 'report'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/report/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidReport'] is True
        assert project.status == 'report review'

    @pytest.mark.django_db
    def test_report_patch__wrong_stage(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.report.check is False
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/report/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'

    @pytest.mark.django_db
    def test_report_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'prereport'
        project.save()

        assert project.report.upload.name is None
        assert project.status == 'prereport'

        user = self.login(project.engineering.user)

        report_image = SimpleUploadedFile(
            name='report.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/report/?projectId=1',
            data={'upload': report_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'report'

    @pytest.mark.django_db
    def test_report_put__wrong_stage(self):
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.report.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        report_image = SimpleUploadedFile(
            name='report.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/report/?projectId=1',
            data={'upload': report_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'



class TestSignatureViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_signature_patch__not_supported(self):
        project = ProjectSignatureStageFactory()

        assert project.status == 'offer accepted'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/signature/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'offer accepted'

    @pytest.mark.django_db
    def test_signature_put__base_case(self):
        project = ProjectSignatureStageFactory()

        assert project.signature.upload.name is None
        assert project.status == 'offer accepted'

        user = self.login(project.engineering.user)

        signature_image = SimpleUploadedFile(
            name='contract_signed.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/signature/?projectId=1',
            data={'upload': signature_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'signature'


    @pytest.mark.django_db
    def test_signature_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.signature.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        signature_image = SimpleUploadedFile(
            name='contract_signed.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/signature/?projectId=1',
            data={'upload': signature_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestPermitViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_permit_patch__not_supported(self):
        project = ProjectPermitStageFactory()

        assert project.status == 'signature'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/permit/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'signature'


    @pytest.mark.django_db
    def test_permit_put__base_case(self):
        project = ProjectPermitStageFactory()

        assert project.permit.upload.name is None
        assert project.status == 'signature'

        user = self.login(project.engineering.user)

        permit_image = SimpleUploadedFile(
            name='permit.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/permit/?projectId=1',
            data={'upload': permit_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'construction permit'


    @pytest.mark.django_db
    def test_permit_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.permit.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        permit_image = SimpleUploadedFile(
            name='permit.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.put(
            path='/somsolet-api/permit/?projectId=1',
            data={'upload': permit_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestOfferViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_offer_patch__not_supported(self):
        project = ProjectOfferStageFactory()

        assert project.status == 'report'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/offer/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'report'
  
    @pytest.mark.django_db
    def test_offer_put__base_case(self):
        project = ProjectOfferStageFactory()

        assert project.offer.upload.name is None
        assert project.status == 'report'

        user = self.login(project.engineering.user)

        offer_image = SimpleUploadedFile(
            name='offer.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/offer/?projectId=1',
            data={'upload': offer_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'offer review'

    @pytest.mark.django_db
    def test_offer_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.permit.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        offer_image = SimpleUploadedFile(
            name='offer.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/offer/?projectId=1',
            data={'upload': offer_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestOfferAcceptedViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_offer_accepted_patch__supported(self):
        project = ProjectOfferAcceptedStageFactory()
        assert project.status == 'offer review'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/offer_accepted/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'offer accepted'
  
    @pytest.mark.django_db
    def test_offer_put__not_supported(self):
        project = ProjectOfferAcceptedStageFactory()
        assert project.status == 'offer review'

        user = self.login(project.engineering.user)

        offer_image = SimpleUploadedFile(
            name='offer.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/offer_accepted/?projectId=1',
            data={'upload': offer_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'offer review'


class TestSecondInvoiceViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_second_invoice_patch__not_supported(self):
        project = ProjectSecondInvoiceStageFactory()

        assert project.status == 'end installation'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/second_invoice/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'end installation'


    @pytest.mark.django_db
    def test_second_invoice_put__base_case(self):
        project = ProjectSecondInvoiceStageFactory()

        assert project.second_invoice.upload.name is None
        assert project.status == 'end installation'

        user = self.login(project.engineering.user)

        second_invoice_image = SimpleUploadedFile(
            name='second_invoice.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/second_invoice/?projectId=1',
            data={'upload': second_invoice_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'second invoice'

    @pytest.mark.django_db
    def test_second_invoice_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.second_invoice.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        second_invoice_image = SimpleUploadedFile(
            name='second_invoice.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/second_invoice/?projectId=1',
            data={'upload': second_invoice_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestLegalRegistrationViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)
        return user

    @pytest.mark.django_db
    def test_legal_registration_patch__not_supported(self):
        project = ProjectLegalRegistrationStageFactory()

        assert project.status == 'end installation'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/legal_registration/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'end installation'


    @pytest.mark.django_db
    def test_legal_registration_put__base_case(self):
        project = ProjectLegalRegistrationStageFactory()

        assert project.legal_registration.upload.name is None
        assert project.status == 'end installation'

        user = self.login(project.engineering.user)

        legal_registration_image = SimpleUploadedFile(
            name='legal_registration.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/legal_registration/?projectId=1',
            data={'upload': legal_registration_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'legal registration'

    @pytest.mark.django_db
    def test_legal_registration_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.legal_registration.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        legal_registration_image = SimpleUploadedFile(
            name='legal_registration.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/legal_registration/?projectId=1',
            data={'upload': legal_registration_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestLegalizationViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)
        return user

    @pytest.mark.django_db
    def test_legalization_patch__not_supported(self):
        project = ProjectLegalizationStageFactory()

        assert project.status == 'last payment'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/legalization/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'last payment'


    @pytest.mark.django_db
    def test_legalization_put__base_case(self):
        project = ProjectLegalizationStageFactory()

        assert project.legalization.rac_file.name is None
        assert project.legalization.ritsic_file.name is None
        assert project.legalization.cie_file.name is None
        assert project.status == 'last payment'

        user = self.login(project.engineering.user)

        legalization_RAC = SimpleUploadedFile(
            name='RAC.jpg', content=b'something', content_type="image/jpeg"
        )
        legalization_RITSIC = SimpleUploadedFile(
            name='RITSIC.jpg', content=b'something', content_type="image/jpeg"
        )
        legalization_CIE = SimpleUploadedFile(
            name='CIE.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/legalization/?projectId=1',
            data={
                'rac_file': legalization_RAC,
                'ritsic_file': legalization_RITSIC,
                'cie_file': legalization_CIE
            },
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'legalization'


    @pytest.mark.django_db
    def test_legalization_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.legalization.rac_file.name is None
        assert project.legalization.ritsic_file.name is None
        assert project.legalization.cie_file.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        legalization_image = SimpleUploadedFile(
            name='legalization.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/legalization/?projectId=1',
            data={'upload': legalization_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestDeliveryCertificateViewSet(LoginMixin, APITestCase):

    def login(self, user):
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)
        super().login(user)

        return user

    @pytest.mark.django_db
    def test_delivery_certificate_patch__not_supported(self):
        project = ProjectDeliveryCertificateStageFactory()

        assert project.status == 'date installation set'

        user = self.login(project.engineering.user)

        response = self.client.patch(
            '/somsolet-api/delivery_certificate/?projectId=1',
            data={'is_checked': True},
            format='json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'date installation set'


    @pytest.mark.django_db
    def test_delivery_certificate_put__base_case(self):
        project = ProjectDeliveryCertificateStageFactory()

        assert project.delivery_certificate.upload.name is None
        assert project.status == 'date installation set'

        user = self.login(project.engineering.user)

        delivery_certificate_image = SimpleUploadedFile(
            name='delivery_certificate.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/delivery_certificate/?projectId=1',
            data={'upload': delivery_certificate_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert project.status == 'end installation'

    @pytest.mark.django_db
    def test_delivery_certificate_put__wrong_stage(self):
        project = ProjectEmptyStatusStageFactory()

        assert project.delivery_certificate.upload.name is None
        assert project.status == 'empty status'

        user = self.login(project.engineering.user)

        delivery_certificate_image = SimpleUploadedFile(
            name='delivery_certificate.jpg', content=b'something', content_type="image/jpeg"
        )
        # TODO: request.data is {} on backend, see issue: https://github.com/encode/django-rest-framework/issues/3951
        response = self.client.generic(method="PUT",
            path='/somsolet-api/delivery_certificate/?projectId=1',
            data={'upload': delivery_certificate_image},
            content_type='multipart/form-data'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'

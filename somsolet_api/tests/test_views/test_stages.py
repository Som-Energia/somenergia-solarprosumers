import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from somsolet.tests.factories import ProjectFactory, UserFactory


class TestPrereportViewSet(TestCase):

    def login(self):

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        return user

    @pytest.mark.django_db
    def test_prereport_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'registered'
        project.save()

        assert project.prereport.check is False
        assert project.status == 'registered'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': False},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidPrereport'] is False
        assert project.status == 'prereport'

    @pytest.mark.django_db
    def test_prereport_patch__review_status(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'prereport'
        project.save()

        assert project.status == 'prereport'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['invalidPrereport'] is True
        assert project.status == 'prereport review'

    @pytest.mark.django_db
    def test_prereport_patch__wrong_stage(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.prereport.check is False
        assert project.status == 'empty status'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'

    @pytest.mark.django_db
    def test_prereport_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'registered'
        project.save()

        assert project.prereport.upload.name is None
        assert project.status == 'registered'

        user = self.login()

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
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.prereport.upload.name is None
        assert project.status == 'empty status'

        user = self.login()

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


class TestSignatureViewSet(TestCase):

    def login(self):

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        return user

    @pytest.mark.django_db
    def test_permit_patch__not_supported(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'
        project.save()

        assert project.status == 'offer'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/signature/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'offer'

    @pytest.mark.django_db
    def test_signature_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'
        project.save()

        assert project.signature.upload.name is None
        assert project.status == 'offer'

        user = self.login()

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
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.signature.upload.name is None
        assert project.status == 'empty status'

        user = self.login()

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


class TestPermitViewSet(TestCase):

    def login(self):

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        return user

    @pytest.mark.django_db
    def test_permit_patch__not_supported(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'signature'
        project.save()

        assert project.status == 'signature'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/permit/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'signature'


    @pytest.mark.django_db
    def test_permit_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'signature'
        project.save()

        assert project.permit.upload.name is None
        assert project.status == 'signature'

        user = self.login()

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
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.permit.upload.name is None
        assert project.status == 'empty status'

        user = self.login()

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
        assert response.status_code == 409
        assert project.status == 'empty status'


class TestLegalRegistrationViewSet(TestCase):

    def login(self):

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        return user

    @pytest.mark.django_db
    def test_legal_registration_patch__not_supported(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'end installation'
        project.save()

        assert project.status == 'end installation'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/legal_registration/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'end installation'


    @pytest.mark.django_db
    def test_legal_registration_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'end installation'
        project.save()

        assert project.legal_registration.upload.name is None
        assert project.status == 'end installation'

        user = self.login()

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
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.legal_registration.upload.name is None
        assert project.status == 'empty status'

        user = self.login()

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

class TestLegalizationViewSet(TestCase):

    def login(self):
        # Extract in BaseTestViewSet (?)
        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        return user

    @pytest.mark.django_db
    def test_legalization_patch__not_supported(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'last payment'
        project.save()

        assert project.status == 'last payment'

        user = self.login()

        response = self.client.patch(
            '/somsolet-api/legalization/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 400
        assert project.status == 'last payment'


    @pytest.mark.django_db
    def test_legalization_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'last payment'
        project.save()

        assert project.legalization.rac_file.name is None
        assert project.legalization.ritsic_file.name is None
        assert project.legalization.cie_file.name is None
        assert project.status == 'last payment'

        user = self.login()

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
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.legalization.rac_file.name is None
        assert project.legalization.ritsic_file.name is None
        assert project.legalization.cie_file.name is None
        assert project.status == 'empty status'

        user = self.login()

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
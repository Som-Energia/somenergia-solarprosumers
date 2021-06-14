import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from somsolet.tests.factories import ProjectFactory, UserFactory


class TestSignatureViewSet(TestCase):

    @pytest.mark.django_db
    def test_signature_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'
        project.save()

        assert project.signature.check is False
        assert project.status == 'offer'

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        response = self.client.patch(
            '/somsolet-api/signature/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 200
        assert response.data['signed'] is True
        assert project.status == 'signature'

    @pytest.mark.django_db
    def test_signature_patch__wrong_stage(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.signature.check is False
        assert project.status == 'empty status'

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        response = self.client.patch(
            '/somsolet-api/signature/?projectId=1',
            data={'is_checked': True},
            content_type='application/json'
        )

        project.refresh_from_db()
        assert response.status_code == 409
        assert project.status == 'empty status'

    @pytest.mark.django_db
    def test_signature_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'
        project.save()

        assert project.signature.upload.name is None
        assert project.status == 'offer'

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

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

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

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

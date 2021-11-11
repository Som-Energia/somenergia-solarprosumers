
import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from somsolet.tests.factories import (ProjectFactory, TechnicalDetailsFactory,
                                      UserFactory)


class TestTechnicalDetailsViewSet(TestCase):

    @pytest.mark.django_db
    def test_technical_details__base_case(self):
        technical_details = TechnicalDetailsFactory()

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_technical_details')
        user.user_permissions.add(permission)

        request = self.client.get(
            '/somsolet-api/technical_details/',
        )
        assert request.status_code == 200
        assert request.data['data']['count'] == 1

    @pytest.mark.django_db
    def test_technical_details__by_project_id(self):
        technical_details = TechnicalDetailsFactory()

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_technical_details')
        user.user_permissions.add(permission)

        request = self.client.get(
            '/somsolet-api/technical_details/?projectId={}'.format(
                technical_details.project.id
            ),
        )
        assert request.status_code == 200
        assert request.data['data']['count'] == 1


class TestInvoicesViewSet(TestCase):

    @pytest.mark.django_db
    def test_last_invoice_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.is_paid_last_invoice is False

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)

        request = self.client.patch(
            '/somsolet-api/last_invoice/?projectId=1',
            data={'is_paid_last_invoice': True},
            content_type='application/json'
        )
        assert request.status_code == 200
        assert request.data['is_paid_last_invoice'] is True

    @pytest.mark.django_db
    def test_last_invoice_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.upload_last_invoice.name is None

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='change_project')
        user.user_permissions.add(permission)

        invoice_image = SimpleUploadedFile(
            name='invoice.jpg', content=b'something', content_type="image/jpeg"
        )
        request = self.client.generic(method="PUT",
            path='/somsolet-api/last_invoice/?projectId=1',
            data={'upload_last_invoice': invoice_image},
            content_type='multipart/form-data'
        )
        assert request.status_code == 200
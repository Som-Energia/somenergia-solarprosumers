
import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from somsolet.tests.factories import (ProjectFactory, TechnicalDetailsFactory,
                                      UserFactory)


class TestProjectViewSet(TestCase):

    @pytest.mark.django_db
    def test_prereport_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.is_invalid_prereport is False

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        request = self.client.patch(
            '/somsolet-api/prereport/?projectId=1',
            data={'is_invalid_prereport': True},
            content_type='application/json'
        )
        assert request.status_code == 200
        assert request.data['is_invalid_prereport'] is True

    @pytest.mark.django_db
    def test_report_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.is_invalid_report is False

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        request = self.client.patch(
            '/somsolet-api/report/?projectId=1',
            data={'is_invalid_report': True},
            content_type='application/json'
        )
        assert request.status_code == 200
        assert request.data['is_invalid_report'] is True

    @pytest.mark.django_db
    def test_prereport_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.upload_prereport.name is None

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        prereport_image = SimpleUploadedFile(
            name='prereport.jpg', content=b'something', content_type="image/jpeg"
        )
        request = self.client.generic(method="PUT",
            path='/somsolet-api/prereport/?projectId=1',
            data={'upload_prereport': prereport_image},
            content_type='multipart/form-data'
        )
        assert request.status_code == 200

    @pytest.mark.django_db
    def test_report_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.upload_prereport.name is None

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        report_image = SimpleUploadedFile(
            "report.jpg", b"file_content", content_type="image/jpeg"
        )
        request = self.client.put(
            '/somsolet-api/report/?projectId=1',
            data={'upload_report': report_image},
            content_type='multipart/form-data'
        )
        assert request.status_code == 200


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
    def test_first_invoice_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.is_payed_first_invoice is False

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        request = self.client.patch(
            '/somsolet-api/first_invoice/?projectId=1',
            data={'is_payed_first_invoice': True},
            content_type='application/json'
        )
        assert request.status_code == 200
        assert request.data['is_payed_first_invoice'] is True

    @pytest.mark.django_db
    def test_first_invoice_put__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()

        assert project.upload_first_invoice.name is None

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        invoice_image = SimpleUploadedFile(
            name='invoice.jpg', content=b'something', content_type="image/jpeg"
        )
        request = self.client.generic(method="PUT",
            path='/somsolet-api/first_invoice/?projectId=1',
            data={'upload_first_invoice': invoice_image},
            content_type='multipart/form-data'
        )
        assert request.status_code == 200

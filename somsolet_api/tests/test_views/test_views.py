import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from somsolet.tests.factories import (
    ProjectFactory,
    ProjectFirstFactory,
    TechnicalDetailsFactory,
    UserFactory,
)
from somsolet_api.tests.common import LoginMixin


class TestTechnicalDetailsViewSet(LoginMixin, TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_technical_details__base_case(self):
        technical_details = TechnicalDetailsFactory()

        user = technical_details.project.engineering.user
        self.login(user)
        permission = Permission.objects.get(codename="view_technical_details")
        user.user_permissions.add(permission)

        permission = Permission.objects.get(codename="view_project")
        user.user_permissions.add(permission)

        request = self.client.get(
            "/somsolet-api/technical_details/",
        )
        assert request.status_code == 200
        assert request.data["data"]["count"] == 1

    @pytest.mark.skip("non-superusers filtering by projectId is not supported")
    def test_technical_details__by_project_id(self):
        technical_details = TechnicalDetailsFactory()

        user = technical_details.project.engineering.user
        self.login(user)
        permission = Permission.objects.get(codename="view_technical_details")
        user.user_permissions.add(permission)

        request = self.client.get(
            f"/somsolet-api/technical_details/?projectId={technical_details.project.id}",
        )
        assert request.status_code == 200
        assert request.data["data"]["count"] == 1


class TestInvoicesViewSet(LoginMixin, TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_first_invoice_patch__base_case(self):
        project = ProjectFirstFactory()

        assert project.is_paid_first_invoice is False

        user = project.engineering.user

        self.login(user)
        permission = Permission.objects.get(codename="change_project")
        user.user_permissions.add(permission)

        request = self.client.patch(
            "/somsolet-api/first_invoice/?projectId=1",
            data={"is_paid_first_invoice": True},
            format="json",
        )
        assert request.status_code == 200
        assert request.data["is_paid_first_invoice"] is True

    def test_last_invoice_patch__base_case(self):
        project = ProjectFirstFactory()

        assert project.is_paid_last_invoice is False

        user = project.engineering.user
        self.login(user)
        permission = Permission.objects.get(codename="change_project")
        user.user_permissions.add(permission)

        request = self.client.patch(
            "/somsolet-api/last_invoice/?projectId=1",
            data={"is_paid_last_invoice": True},
            format="json",
        )
        assert request.status_code == 200
        assert request.data["is_paid_last_invoice"] is True

    def test_first_invoice_put__base_case(self):
        project = ProjectFirstFactory()

        assert project.upload_first_invoice.name is None

        user = project.engineering.user
        self.login(user)
        permission = Permission.objects.get(codename="change_project")
        user.user_permissions.add(permission)

        invoice_image = SimpleUploadedFile(
            name="invoice.jpg", content=b"something", content_type="image/jpeg"
        )
        request = self.client.put(
            path="/somsolet-api/first_invoice/?projectId=1",
            data={"upload_first_invoice": invoice_image},
            content_type="multipart/form-data",
        )
        assert request.status_code == 200

    def test_last_invoice_put__base_case(self):
        project = ProjectFirstFactory()

        assert project.upload_last_invoice.name is None

        user = project.engineering.user
        self.login(user)
        permission = Permission.objects.get(codename="change_project")
        user.user_permissions.add(permission)

        invoice_image = SimpleUploadedFile(
            name="invoice.jpg", content=b"something", content_type="image/jpeg"
        )
        request = self.client.put(
            path="/somsolet-api/last_invoice/?projectId=1",
            data={"upload_last_invoice": invoice_image},
            content_type="multipart/form-data",
        )

        assert request.status_code == 200

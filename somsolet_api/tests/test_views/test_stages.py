import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from somsolet.tests.factories import (ProjectFactory, UserFactory)

class TestSignatureViewSet(TestCase):

    @pytest.mark.django_db
    def test_signature_patch__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.save()
        assert project.signature.check is False

        user = UserFactory()
        user.set_password('1234')
        user.save()
        self.client.login(username=user.username, password='1234')
        permission = Permission.objects.get(codename='view_project')
        user.user_permissions.add(permission)

        response = self.client.patch(
            '/somsolet-api/signature/?projectId=1',
            data={'signed': True},
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.data['signed'] is True

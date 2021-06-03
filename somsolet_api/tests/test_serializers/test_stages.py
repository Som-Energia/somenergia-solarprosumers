import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import ProjectFactory
from somsolet_api.serializer import SignatureFileSerializer


class TestSignatureFileSerializer:

    @pytest.mark.django_db
    def test_signature_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        signature_serializer = SignatureFileSerializer(
            instance=project
        )

        assert signature_serializer.data == dict(
            id=1,
            signatureDate='2021-06-01',
            signatureUpload=None,
            signed=False,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_signature_file_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.signature.check = True
        project.status = 'signature'

        signature_serializer = SignatureFileSerializer(
            instance=project
        )

        assert signature_serializer.data == dict(
            id=1,
            signatureDate='2021-06-01',
            signatureUpload=None,
            signed=True,
            status='signature'
        )

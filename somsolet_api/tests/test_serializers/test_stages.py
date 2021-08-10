import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import ProjectFactory
from somsolet_api.serializer import SignatureFileSerializer, PermitFileSerializer, OfferFileSerializer


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

    @pytest.mark.django_db
    def test_signature_file_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.signature.check = True
        project.status = 'signature'
        signature_image = SimpleUploadedFile(
            "signature.jpg", b"file_content", content_type="image/jpeg"
        )
        project.signature.upload = signature_image
        signature_serializer = SignatureFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert signature_serializer.data == dict(
            id=1,
            signatureDate='2021-06-01',
            signatureUpload='/uploaded_files/signature.jpg',
            signed=True,
            status='signature'
        )


class TestPermitFileSerializer:

    @pytest.mark.django_db
    def test_permit_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        permit_serializer = PermitFileSerializer(
            instance=project
        )

        assert permit_serializer.data == dict(
            id=1,
            permitDate='2021-06-01',
            permitUpload=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_permit_file_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'construction permit'

        permit_serializer = PermitFileSerializer(
            instance=project
        )

        assert permit_serializer.data == dict(
            id=1,
            permitDate='2021-06-01',
            permitUpload=None,
            status='construction permit'
        )

    @pytest.mark.django_db
    def test_permit_file_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'construction permit'
        permit_image = SimpleUploadedFile(
            "permit.jpg", b"file_content", content_type="image/jpeg"
        )
        project.permit.upload = permit_image
        permit_serializer = PermitFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert permit_serializer.data == dict(
            id=1,
            permitDate='2021-06-01',
            permitUpload='/uploaded_files/permit.jpg',
            status='construction permit'
        )


class TestOfferFileSerializer:

    @pytest.mark.django_db
    def test_offer_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        offer_serializer = OfferFileSerializer(
            instance=project
        )

        assert offer_serializer.data == dict(
            id=1,
            offerDate='2021-06-29',
            offerUpload=None,
            isOfferAccepted=False,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_offer_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'

        offer_serializer = OfferFileSerializer(
            instance=project
        )

        assert offer_serializer.data == dict(
            id=1,
            isOfferAccepted=False,
            offerDate='2021-06-29',
            offerUpload=None,
            status='offer'
        )

    @pytest.mark.django_db
    def test_offer_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer'
        offer_image = SimpleUploadedFile(
            "offer.jpg", b"file_content", content_type="image/jpeg"
        )
        project.offer.upload = offer_image
        offer_serializer = OfferFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert offer_serializer.data == dict(
            id=1,
            offerDate='2021-06-29',
            offerUpload='/uploaded_files/offer.jpg',
            isOfferAccepted=False,
            status='offer'
        )

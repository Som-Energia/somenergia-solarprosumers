import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import ProjectFactory
from somsolet_api.serializer import SignatureFileSerializer, PermitFileSerializer, OfferReviewFileSerializer


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


class TestOfferReviewFileSerializer:

    @pytest.mark.django_db
    def test_offer_review_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        offer_review_serializer = OfferReviewFileSerializer(
            instance=project
        )

        assert offer_review_serializer.data == dict(
            id=1,
            offerReviewDate='2021-06-29',
            offerReviewUpload=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_offer_review_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer_review'

        offer_review_serializer = OfferReviewFileSerializer(
            instance=project
        )

        assert offer_review_serializer.data == dict(
            id=1,
            offerReviewDate='2021-06-29',
            offerReviewUpload=None,
            status='offer_review'
        )

    @pytest.mark.django_db
    def test_offer_review_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'offer_review'
        offer_review_image = SimpleUploadedFile(
            "offer_review.jpg", b"file_content", content_type="image/jpeg"
        )
        project.offer_review.upload = offer_review_image
        offer_review_serializer = OfferReviewFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert offer_review_serializer.data == dict(
            id=1,
            offerReviewDate='2021-06-29',
            offerReviewUpload='/uploaded_files/offer_review.jpg',
            status='offer_review'
        )

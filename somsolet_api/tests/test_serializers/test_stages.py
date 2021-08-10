import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import ProjectFactory
from somsolet_api.serializer import (SignatureFileSerializer, PermitFileSerializer,
                                     LegalRegistrationFileSerializer, LegalizationFileSerializer,
                                     PrereportFileSerializer)



class TestPrereportFileSerializer:

    @pytest.mark.django_db
    def test_prereport_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        prereport_serializer = PrereportFileSerializer(
            instance=project
        )

        assert prereport_serializer.data == dict(
            id=1,
            prereportDate='2021-06-01',
            prereportUpload=None,
            invalidPrereport=False,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_prereport_file_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.prereport.check = True
        project.status = 'prereport'

        prereport_serializer = PrereportFileSerializer(
            instance=project
        )

        assert prereport_serializer.data == dict(
            id=1,
            prereportDate='2021-06-01',
            prereportUpload=None,
            invalidPrereport=True,
            status='prereport'
        )

    @pytest.mark.django_db
    def test_prereport_file_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.prereport.check = True
        project.status = 'prereport'
        prereport_image = SimpleUploadedFile(
            "prereport.jpg", b"file_content", content_type="image/jpeg"
        )
        project.prereport.upload = prereport_image
        prereport_serializer = PrereportFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert prereport_serializer.data == dict(
            id=1,
            prereportDate='2021-06-01',
            prereportUpload='/uploaded_files/prereport.jpg',
            invalidPrereport=True,
            status='prereport'
        )


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


class TestLegalRegistrationFileSerializer:

    @pytest.mark.django_db
    def test_legal_registration_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        legal_registration_serializer = LegalRegistrationFileSerializer(
            instance=project
        )

        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate='2021-06-01',
            legalRegistrationUpload=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_legal_registration_file_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'legal registration'

        legal_registration_serializer = LegalRegistrationFileSerializer(
            instance=project
        )

        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate='2021-06-01',
            legalRegistrationUpload=None,
            status='legal registration'
        )

    @pytest.mark.django_db
    def test_legal_registration_file_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'legal registration'
        legal_registration_image = SimpleUploadedFile(
            "legal_registration.jpg", b"file_content", content_type="image/jpeg"
        )
        project.legal_registration.upload = legal_registration_image
        legal_registration_serializer = LegalRegistrationFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate='2021-06-01',
            legalRegistrationUpload='/uploaded_files/legal_registration.jpg',
            status='legal registration'
        )


class TestLegalizationFileSerializer:

    @pytest.mark.django_db
    def test_legalization_file_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        legalization_serializer = LegalizationFileSerializer(
            instance=project
        )

        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate='2021-06-01',
            legalizationRac=None,
            legalizationRitsic=None,
            legalizationCie=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_legalization_file_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'legalization'

        legalization_serializer = LegalizationFileSerializer(
            instance=project
        )

        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate='2021-06-01',
            legalizationRac=None,
            legalizationRitsic=None,
            legalizationCie=None,
            status='legalization'
        )

    @pytest.mark.django_db
    def test_legalization_file_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'legalization'
        legalization_RAC = SimpleUploadedFile(
            name='RAC.jpg', content=b'something', content_type="image/jpeg"
        )
        legalization_RITSIC = SimpleUploadedFile(
            name='RITSIC.jpg', content=b'something', content_type="image/jpeg"
        )
        legalization_CIE = SimpleUploadedFile(
            name='CIE.jpg', content=b'something', content_type="image/jpeg"
        )
        project.legalization.rac_file = legalization_RAC
        project.legalization.ritsic_file = legalization_RITSIC
        project.legalization.cie_file = legalization_CIE
        legalization_serializer = LegalizationFileSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate='2021-06-01',
            legalizationRac='/uploaded_files/RAC.jpg',
            legalizationRitsic='/uploaded_files/RITSIC.jpg',
            legalizationCie='/uploaded_files/CIE.jpg',
            status='legalization'
        )

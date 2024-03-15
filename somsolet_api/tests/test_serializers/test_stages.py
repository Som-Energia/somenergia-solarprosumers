import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import ProjectFactory
from somsolet_api.serializer import (
    SignatureStageSerializer,
    PermitStageSerializer,
    LegalRegistrationStageSerializer,
    LegalizationStageSerializer,
    PrereportStageSerializer,
    ReportStageSerializer,
    OfferStageSerializer,
    OfferAcceptedStageSerializer,
    SecondInvoiceStageSerializer,
    DeliveryCertificateStageSerializer,
)


class TestPrereportStageSerializer:
    @pytest.mark.django_db
    def test_prereport_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        prereport_serializer = PrereportStageSerializer(instance=project)

        assert prereport_serializer.data == dict(
            id=1,
            prereportDate="2021-06-01",
            prereportUpload=None,
            invalidPrereport=False,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_prereport_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.prereport.check = True
        project.status = "prereport"

        prereport_serializer = PrereportStageSerializer(instance=project)

        assert prereport_serializer.data == dict(
            id=1,
            prereportDate="2021-06-01",
            prereportUpload=None,
            invalidPrereport=True,
            status="prereport",
        )

    @pytest.mark.django_db
    def test_prereport_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.prereport.check = True
        project.status = "prereport"
        prereport_image = SimpleUploadedFile(
            "prereport.jpg", b"file_content", content_type="image/jpeg"
        )
        project.prereport.upload = prereport_image
        prereport_serializer = PrereportStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert prereport_serializer.data == dict(
            id=1,
            prereportDate="2021-06-01",
            prereportUpload="/uploaded_files/prereport.jpg",
            invalidPrereport=True,
            status="prereport",
        )


class TestReportStageSerializer:
    @pytest.mark.django_db
    def test_report_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        report_serializer = ReportStageSerializer(instance=project)

        assert report_serializer.data == dict(
            id=1,
            reportDate="2021-06-01",
            reportUpload=None,
            invalidReport=False,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_report_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.report.check = True
        project.status = "report"

        report_serializer = ReportStageSerializer(instance=project)

        assert report_serializer.data == dict(
            id=1,
            reportDate="2021-06-01",
            reportUpload=None,
            invalidReport=True,
            status="report",
        )

    @pytest.mark.django_db
    def test_report_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.report.check = True
        project.status = "report"
        report_image = SimpleUploadedFile(
            "report.jpg", b"file_content", content_type="image/jpeg"
        )
        project.report.upload = report_image
        report_serializer = ReportStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert report_serializer.data == dict(
            id=1,
            reportDate="2021-06-01",
            reportUpload="/uploaded_files/report.jpg",
            invalidReport=True,
            status="report",
        )


class TestSignatureStageSerializer:
    @pytest.mark.django_db
    def test_signature_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        signature_serializer = SignatureStageSerializer(instance=project)

        assert signature_serializer.data == dict(
            id=1,
            signatureDate="2021-06-01",
            signatureUpload=None,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_signature_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.signature.check = True
        project.status = "signature"

        signature_serializer = SignatureStageSerializer(instance=project)

        assert signature_serializer.data == dict(
            id=1, signatureDate="2021-06-01", signatureUpload=None, status="signature"
        )

    @pytest.mark.django_db
    def test_signature_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.signature.check = True
        project.status = "signature"
        signature_image = SimpleUploadedFile(
            "signature.jpg", b"file_content", content_type="image/jpeg"
        )
        project.signature.upload = signature_image
        signature_serializer = SignatureStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert signature_serializer.data == dict(
            id=1,
            signatureDate="2021-06-01",
            signatureUpload="/uploaded_files/signature.jpg",
            status="signature",
        )


class TestPermitStageSerializer:
    @pytest.mark.django_db
    def test_permit_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        permit_serializer = PermitStageSerializer(instance=project)

        assert permit_serializer.data == dict(
            id=1, permitDate="2021-06-01", permitUpload=None, status="empty status"
        )

    @pytest.mark.django_db
    def test_permit_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "construction permit"

        permit_serializer = PermitStageSerializer(instance=project)

        assert permit_serializer.data == dict(
            id=1,
            permitDate="2021-06-01",
            permitUpload=None,
            status="construction permit",
        )

    @pytest.mark.django_db
    def test_permit_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "construction permit"
        permit_image = SimpleUploadedFile(
            "permit.jpg", b"file_content", content_type="image/jpeg"
        )
        project.permit.upload = permit_image
        permit_serializer = PermitStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert permit_serializer.data == dict(
            id=1,
            permitDate="2021-06-01",
            permitUpload="/uploaded_files/permit.jpg",
            status="construction permit",
        )


class TestOfferStageSerializer:
    @pytest.mark.django_db
    def test_offer_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        offer_serializer = OfferStageSerializer(instance=project)

        assert offer_serializer.data == dict(
            id=1, offerDate="2021-06-29", offerUpload=None, status="empty status"
        )

    @pytest.mark.django_db
    def test_offer_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "offer review"

        offer_serializer = OfferStageSerializer(instance=project)

        assert offer_serializer.data == dict(
            id=1, offerDate="2021-06-29", offerUpload=None, status="offer review"
        )

    @pytest.mark.django_db
    def test_offer_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "offer review"
        offer_image = SimpleUploadedFile(
            "offer.jpg", b"file_content", content_type="image/jpeg"
        )
        project.offer.upload = offer_image
        offer_serializer = OfferStageSerializer(instance=project)
        # TODO: find out how to create directories with factories
        assert offer_serializer.data == dict(
            id=1,
            offerDate="2021-06-29",
            offerUpload="/uploaded_files/offer.jpg",
            status="offer review",
        )


class TestOfferAcceptedStageSerializer:
    @pytest.mark.django_db
    def test_offer_accepted_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        offer_serializer = OfferAcceptedStageSerializer(instance=project)

        assert offer_serializer.data == dict(
            id=1,
            offerAcceptedDate="2021-06-29",
            isOfferAccepted=False,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_offer_accepted_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.offer_accepted.check = True
        project.status = "offer accepted"

        offer_serializer = OfferAcceptedStageSerializer(instance=project)

        assert offer_serializer.data == dict(
            id=1,
            offerAcceptedDate="2021-06-29",
            isOfferAccepted=True,
            status="offer accepted",
        )


class TestSecondInvoiceStageSerializer:
    @pytest.mark.django_db
    def test_second_invoice_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        second_invoice_serializer = SecondInvoiceStageSerializer(instance=project)

        assert second_invoice_serializer.data == dict(
            id=1,
            secondInvoiceDate="2021-06-29",
            secondInvoiceUpload=None,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_second_invoice_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "end installation"

        second_invoice_serializer = SecondInvoiceStageSerializer(instance=project)

        assert second_invoice_serializer.data == dict(
            id=1,
            secondInvoiceDate="2021-06-29",
            secondInvoiceUpload=None,
            status="end installation",
        )

    @pytest.mark.django_db
    def test_second_invoice_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "end installation"
        second_invoice_image = SimpleUploadedFile(
            "second_invoice.jpg", b"file_content", content_type="image/jpeg"
        )
        project.second_invoice.upload = second_invoice_image
        second_invoice_serializer = SecondInvoiceStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert second_invoice_serializer.data == dict(
            id=1,
            secondInvoiceDate="2021-06-29",
            secondInvoiceUpload="/uploaded_files/second_invoice.jpg",
            status="end installation",
        )


class TestLegalRegistrationStageSerializer:
    @pytest.mark.django_db
    def test_legal_registration_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        legal_registration_serializer = LegalRegistrationStageSerializer(
            instance=project
        )

        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate="2021-06-01",
            legalRegistrationUpload=None,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_legal_registration_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "legal registration"

        legal_registration_serializer = LegalRegistrationStageSerializer(
            instance=project
        )

        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate="2021-06-01",
            legalRegistrationUpload=None,
            status="legal registration",
        )

    @pytest.mark.django_db
    def test_legal_registration_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "legal registration"
        legal_registration_image = SimpleUploadedFile(
            "legal_registration.jpg", b"file_content", content_type="image/jpeg"
        )
        project.legal_registration.upload = legal_registration_image
        legal_registration_serializer = LegalRegistrationStageSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert legal_registration_serializer.data == dict(
            id=1,
            legalRegistrationDate="2021-06-01",
            legalRegistrationUpload="/uploaded_files/legal_registration.jpg",
            status="legal registration",
        )


class TestLegalizationStageSerializer:
    @pytest.mark.django_db
    def test_legalization_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        legalization_serializer = LegalizationStageSerializer(instance=project)

        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate="2021-06-01",
            legalizationRac=None,
            legalizationRitsic=None,
            legalizationCie=None,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_legalization_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "legalization"

        legalization_serializer = LegalizationStageSerializer(instance=project)

        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate="2021-06-01",
            legalizationRac=None,
            legalizationRitsic=None,
            legalizationCie=None,
            status="legalization",
        )

    @pytest.mark.django_db
    def test_legalization_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "legalization"
        legalization_RAC = SimpleUploadedFile(
            name="RAC.jpg", content=b"something", content_type="image/jpeg"
        )
        legalization_RITSIC = SimpleUploadedFile(
            name="RITSIC.jpg", content=b"something", content_type="image/jpeg"
        )
        legalization_CIE = SimpleUploadedFile(
            name="CIE.jpg", content=b"something", content_type="image/jpeg"
        )
        project.legalization.rac_file = legalization_RAC
        project.legalization.ritsic_file = legalization_RITSIC
        project.legalization.cie_file = legalization_CIE
        legalization_serializer = LegalizationStageSerializer(instance=project)

        # TODO: find out how to create directories with factories
        assert legalization_serializer.data == dict(
            id=1,
            legalizationDate="2021-06-01",
            legalizationRac="/uploaded_files/RAC.jpg",
            legalizationRitsic="/uploaded_files/RITSIC.jpg",
            legalizationCie="/uploaded_files/CIE.jpg",
            status="legalization",
        )


class TestDeliveryCertificateStageSerializer:
    @pytest.mark.django_db
    def test_delivery_certificate_stage_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        delivery_certificate_serializer = DeliveryCertificateStageSerializer(
            instance=project
        )

        assert delivery_certificate_serializer.data == dict(
            id=1,
            deliveryCertificateDate="2021-06-01",
            deliveryCertificateUpload=None,
            status="empty status",
        )

    @pytest.mark.django_db
    def test_delivery_certificate_stage_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "date installation set"

        delivery_certificate_serializer = DeliveryCertificateStageSerializer(
            instance=project
        )

        assert delivery_certificate_serializer.data == dict(
            id=1,
            deliveryCertificateDate="2021-06-01",
            deliveryCertificateUpload=None,
            status="date installation set",
        )

    @pytest.mark.django_db
    def test_delivery_certificate_stage_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.status = "date installation set"
        delivery_certificate_image = SimpleUploadedFile(
            "delivery_certificate.jpg", b"file_content", content_type="image/jpeg"
        )
        project.delivery_certificate.upload = delivery_certificate_image
        delivery_certificate_serializer = DeliveryCertificateStageSerializer(
            instance=project
        )

        # TODO: find out how to create directories with factories
        assert delivery_certificate_serializer.data == dict(
            id=1,
            deliveryCertificateDate="2021-06-01",
            deliveryCertificateUpload="/uploaded_files/delivery_certificate.jpg",
            status="date installation set",
        )

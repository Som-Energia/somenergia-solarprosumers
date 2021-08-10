import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import (CampaignFactory, ProjectFactory,
                                      TechnicalDetailsFactory)
from somsolet_api.serializer import (ReportSerializer,
                                     StatsSerializer,
                                     TechnicalDetailsSerializer,
                                     FirstInvoiceSerializer,
                                     LastInvoiceSerializer)


class TestTechnicalDetailsSerializer:

    @pytest.mark.django_db
    def test_technical_details_serializer__base_case(self):
        serializer = TechnicalDetailsSerializer(
            instance=TechnicalDetailsFactory()
        )
        assert serializer.data['administrative_division'] == 'Barbados'
        assert serializer.data['town'] == 'Speightstown'


class TestReportSerializer:

    @pytest.mark.django_db
    def test_report_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        report_serializer = ReportSerializer(
            instance=project
        )

        assert report_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_report=None,
            is_invalid_report=False,
            upload_report=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_report_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.date_report = '2020-01-01'
        project.status = 'report review'
        report_serializer = ReportSerializer(
            instance=project
        )

        assert report_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_report='2020-01-01',
            is_invalid_report=False,
            upload_report=None,
            status='report review'
        )

    @pytest.mark.django_db
    def test_report_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.date_report = '2020-01-01'
        project.is_invalid_report = True
        project.status = 'report'
        report_image = SimpleUploadedFile(
            "report.jpg", b"file_content", content_type="image/jpeg"
        )
        project.upload_report = report_image
        report_serializer = ReportSerializer(
            instance=project
        )

        assert report_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_report='2020-01-01',
            is_invalid_report=True,
            upload_report='/uploaded_files/report.jpg',
            status='report'
        )

class TestLastInvoiceSerializer:

    @pytest.mark.django_db
    def test_last_invoice_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'legal registration'
        invoice_serializer = LastInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_last_invoice=None,
            is_paid_last_invoice=False,
            upload_last_invoice=None,
            status='legal registration'
        )

    @pytest.mark.django_db
    def test_last_invoice_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.date_last_invoice = '2020-01-01'
        project.status = 'legal registration'
        invoice_serializer = LastInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_last_invoice='2020-01-01',
            is_paid_last_invoice=False,
            upload_last_invoice=None,
            status='legal registration'
        )

    @pytest.mark.django_db
    def test_last_invoice_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.date_last_invoice = '2020-01-01'
        project.is_paid_last_invoice = True
        project.status = 'pending payment'
        invoice_image = SimpleUploadedFile(
            "invoice.jpg", b"file_content", content_type="image/jpeg"
        )
        project.upload_last_invoice = invoice_image
        invoice_serializer = LastInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_last_invoice='2020-01-01',
            is_paid_last_invoice=True,
            upload_last_invoice='/uploaded_files/invoice.jpg',
            status='pending payment'
        )

class TestFirstInvoiceSerializer:

    @pytest.mark.django_db
    def test_first_invoice_serializer__base_case(self):
        project = ProjectFactory()
        project.id = 1
        project.status = 'signature'
        invoice_serializer = FirstInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_first_invoice=None,
            is_paid_first_invoice=False,
            upload_first_invoice=None,
            status='signature'
        )

    @pytest.mark.django_db
    def test_first_invoice_serializer__with_data(self):
        project = ProjectFactory()
        project.id = 1
        project.date_first_invoice = '2020-01-01'
        project.status = 'signature'
        invoice_serializer = FirstInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_first_invoice='2020-01-01',
            is_paid_first_invoice=False,
            upload_first_invoice=None,
            status='signature'
        )

    @pytest.mark.django_db
    def test_first_invoice_serializer__with_attachment(self):
        project = ProjectFactory()
        project.id = 1
        project.date_first_invoice = '2020-01-01'
        project.is_paid_first_invoice = True
        project.status = 'pending payment'
        invoice_image = SimpleUploadedFile(
            "invoice.jpg", b"file_content", content_type="image/jpeg"
        )
        project.upload_first_invoice = invoice_image
        invoice_serializer = FirstInvoiceSerializer(
            instance=project
        )

        assert invoice_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_first_invoice='2020-01-01',
            is_paid_first_invoice=True,
            upload_first_invoice='/uploaded_files/invoice.jpg',
            status='pending payment'
        )


class TestStatsSerializer:

    @pytest.mark.django_db
    def test_stats_serializer__empty_stats(self):
        stats_serializer = StatsSerializer()
        campaign_stats = stats_serializer.get_stats(CampaignFactory())

        assert campaign_stats == {}


    @pytest.mark.django_db
    def test_stats_serializer__with_stats(self):
        stats_serializer = StatsSerializer()
        campaign = CampaignFactory()
        campaign.id = 13
        project = ProjectFactory()
        project.registration_date = '2020-01-04'
        project.status = 'prereport'
        project.save()
        campaign_stats = stats_serializer.get_stats(campaign)

        assert campaign_stats == dict(
            campaignId=13,
            totalInstalations=1,
            totalPower=dict(
                value=3,
                units='kWp'
            ),
            totalGeneration=dict(
                value=0.00435,
                units='GWp/any'
            )
        )

import pytest
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import (CampaignFactory, ProjectFactory, ProjectFirstFactory,
                                      TechnicalDetailsFactory)
from somsolet_api.serializer import (StatsSerializer,
                                     TechnicalDetailsSerializer,
                                     FirstInvoiceSerializer,
                                     LastInvoiceSerializer,
                                     DeliveryCertificateStageSerializer,
                                     ProjectSerializer)


class TestProjectSerializer:
    @pytest.mark.django_db
    def test__base_case(self):
        project = ProjectFirstFactory()
        details = TechnicalDetailsFactory(
            project=project,
        )
        serializer = ProjectSerializer(
            instance=project,
        )
        assert serializer.data['description'] == {
            'campaignName': 'Solar Paco',
            'dateStart': None,
            'engineerings': [],
            'name': 'Instalació plaques Montserrat Escayola',
            'projectId': 1,
            'registeredPerson': {
                'email': 'montse@somenergia.coop',
                'language': 'ca',
                'name': 'Montserrat Escayola',
                'phoneNumber': '631111380',
            },
            'stageId': 'empty status',
            'supplyPoint': {
                'address': {
                    'administrativeDivision': 'Barbados',
                    'municipality': 'Parroquia de Christ Church',
                    'postalCode': '08026',
                    'street': 'Bridgetown Norman',
                    'town': 'Speightstown'
                },
                'cups': 'ES0024123453789101XXYY',
                'tariff': '2.0A',
            },
            'warning': 'No Warn',
        }
        # TODO  assert serializer.data['stages'] == {...}


class TestTechnicalDetailsSerializer:

    @pytest.mark.django_db
    def test_technical_details_serializer__base_case(self):
        serializer = TechnicalDetailsSerializer(
            instance=TechnicalDetailsFactory()
        )
        assert serializer.data['administrative_division'] == 'Barbados'
        assert serializer.data['town'] == 'Speightstown'


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

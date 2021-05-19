import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import (CampaignFactory, ProjectFactory,
                                      TechnicalDetailsFactory)
from somsolet_api.serializer import (PrereportSerializer, ReportSerializer,
                                     StatsSerializer,
                                     TechnicalDetailsSerializer)


class TestTechnicalDetailsSerializer:

    @pytest.mark.django_db
    def test_technical_details_serializer__base_case(self):
        serializer = TechnicalDetailsSerializer(
            instance=TechnicalDetailsFactory()
        )
        assert serializer.data['administrative_division'] == 'Barbados'
        assert serializer.data['project'] == 1


class TestPrereportSerializer:

    @pytest.mark.django_db
    def test_prereport_serializer__base_case(self):
        prereport_serializer = PrereportSerializer(
            instance=ProjectFactory()
        )

        assert prereport_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_prereport=None,
            is_invalid_prereport=False,
            upload_prereport=None,
            status='empty status'
        )

    @pytest.mark.django_db
    def test_prereport_serializer__with_data(self):
        project = ProjectFactory()
        project.date_prereport = '2020-01-01'
        project.status = 'prereport review'
        prereport_serializer = PrereportSerializer(
            instance=project
        )

        assert prereport_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_prereport='2020-01-01',
            is_invalid_prereport=False,
            upload_prereport=None,
            status='prereport review'
        )

    @pytest.mark.django_db
    def test_prereport_serializer__with_attachment(self):
        project = ProjectFactory()
        project.date_prereport = '2020-01-01'
        project.is_invalid_prereport = True
        project.status = 'prereport'
        prereport_image = SimpleUploadedFile(
            "prereport.jpg", b"file_content", content_type="image/jpeg"
        )
        project.upload_prereport = prereport_image
        prereport_serializer = PrereportSerializer(
            instance=project
        )

        assert prereport_serializer.data == dict(
            id=1,
            name='Instalació plaques Montserrat Escayola',
            date_prereport='2020-01-01',
            is_invalid_prereport=True,
            upload_prereport='/uploaded_files/prereport.jpg',
            status='prereport'
        )


class TestReportSerializer:

    @pytest.mark.django_db
    def test_report_serializer__base_case(self):
        report_serializer = ReportSerializer(
            instance=ProjectFactory()
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
        project = ProjectFactory()
        project.registration_date = '2020-01-04'
        project.status = 'prereport'
        project.save()
        campaign_stats = stats_serializer.get_stats(campaign)

        assert campaign_stats == dict(
            total_instalations=1,
            total_power=dict(
                value=3,
                units='kWp'
            ),
            total_generation=dict(
                value=0.00435,
                units='GWp/any'
            )
        )

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from somsolet.tests.factories import CampaignFactory, ProjectFactory
from somsolet_api.serializer import StatsSerializer, PrereportSerializer, ReportSerializer


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



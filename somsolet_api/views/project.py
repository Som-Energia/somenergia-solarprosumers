from rest_framework import status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from schedule.models import Calendar
from somsolet.models import Project, Technical_details
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (DownloadCchSerializer,
                                     FirstInvoiceSerializer,
                                     LastInvoiceSerializer, ProjectSerializer,
                                     RenkontoEventSerializer, ReportSerializer,
                                     TechnicalDetailsSerializer)
from somsolet_api.shortcuts import (not_found_response,
                                    validation_error_response)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')

        user = self.request.headers.get('dni')
        campaign = self.request.query_params.get('campaignId')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif campaign:
            return queryset.filter(campaign__id=campaign)
        elif project:
            return queryset.filter(id=project)
        else:
            return queryset

    @action(detail=True, methods=['put'], name='set_technical_visit')
    def set_technical_visit(self, request, pk):
        project = Project.projects.get_project(pk, request.user)
        if not project:
            return not_found_response()
        technical_visit = RenkontoEventSerializer(
            data=request.data, partial=True, context={'request': request}
        )
        if not technical_visit.is_valid():
            return validation_error_response(technical_visit)

        calendar = Calendar.objects.get_calendar_for_object(project.engineering.user)

        event = technical_visit.set_technical_visit(
            calendar=calendar,
            project=project,
            created_by=request.user
        )

        return Response(technical_visit.to_representation(event))



class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')

        user = self.request.headers.get('dni')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif project:
            return queryset.filter(id=project)
        else:
            return queryset

    def patch(self, request, *args, **kwargs):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        report = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if report.is_valid():
            instance.update_is_invalid_report(request.data.get('is_invalid_report'))
            report.save()
            return Response(report.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        report = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if report.is_valid():
            instance.update_upload_report(request.data.get('upload_report'))
            report.save()
            return Response(report.data, status=status.HTTP_200_OK)
        else:
            return Response(report.errors, status=status.HTTP_400_BAD_REQUEST)


class FirstInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = FirstInvoiceSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')

        user = self.request.headers.get('dni')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif project:
            return queryset.filter(id=project)
        else:
            return queryset

    def patch(self, request, *args, **kwargs):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        invoice = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            instance.update_is_paid_first_invoice(request.data.get('is_paid_first_invoice'))
            invoice.save()
            return Response(invoice.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        invoice = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            instance.update_upload_first_invoice(request.data.get('upload_first_invoice'))
            invoice.save()
            return Response(invoice.data, status=status.HTTP_200_OK)
        else:
            return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)


class LastInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = LastInvoiceSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')

        user = self.request.headers.get('dni')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif project:
            return queryset.filter(id=project)
        else:
            return queryset

    def patch(self, request, *args, **kwargs):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        invoice = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            instance.update_is_paid_last_invoice(request.data.get('is_paid_last_invoice'))
            invoice.save()
            return Response(invoice.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        invoice = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            instance.update_upload_last_invoice(request.data.get('upload_last_invoice'))
            invoice.save()
            return Response(invoice.data, status=status.HTTP_200_OK)
        else:
            return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)


class CchDownloadViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = DownloadCchSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')
        project = self.request.query_params.get('projectId')
        if project:
            return queryset.filter(id=project)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DownloadCchSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class TechnicalDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = TechnicalDetailsSerializer

    def get_queryset(self):
        queryset = Technical_details.objects.all()

        user = self.request.headers.get('dni')
        campaign = self.request.query_params.get('campaignId')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif campaign:
            return queryset.filter(campaign__id=campaign)
        elif project:
            return queryset.filter(project=project)
        else:
            return queryset

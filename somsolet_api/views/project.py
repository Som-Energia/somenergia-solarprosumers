from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response
from somsolet.models import Project
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (DownloadCchSerializer, ReportSerializer,
                                     PrereportSerializer, ProjectSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

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


class PrereportViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = PrereportSerializer

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
        prereport = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if prereport.is_valid():
            instance.update_is_invalid_prereport(request.data.get('is_invalid_prereport'))
            prereport.save()
            return Response(prereport.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        prereport = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if prereport.is_valid():
            instance.update_upload_prereport(request.data.get('upload_prereport'))
            prereport.save()
            return Response(prereport.data, status=status.HTTP_200_OK)
        else:
            return Response(prereport.errors, status=status.HTTP_400_BAD_REQUEST)


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

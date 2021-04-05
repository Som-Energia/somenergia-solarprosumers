from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response
from somsolet.models import Project
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (DownloadCchSerializer,
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

    def patch(self, request, *args, **kwargs):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        serializer = PrereportSerializer(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            instance.is_invalid_prereport = request.data['is_invalid_prereport']
            if instance.is_invalid_prereport:
                instance.status = 'prereport review'
            else:
                instance.status = 'prereport'
            instance.save()
            serializer.save()
            return Response(serializer.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )

        serializer = PrereportSerializer(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.upload_prereport = request.data['upload_prereport']
            instance.date_prereport = datetime.now().strftime('%Y-%m-%d')
            if not instance.is_invalid_prereport:
                instance.status = 'prereport'
            instance.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

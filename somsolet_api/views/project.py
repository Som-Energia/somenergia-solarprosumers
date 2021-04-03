from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response
from somsolet.models import Project
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (DownloadCchSerializer,
                                     PrereportSerializer, ProjectSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.headers.get('dni')

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

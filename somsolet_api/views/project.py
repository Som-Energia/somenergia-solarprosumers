from rest_framework import viewsets
from somsolet.models import Project
from somsolet_api.serializer import ProjectSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.headers.get('dni')
        return Project.objects.filter(client__dni=user)
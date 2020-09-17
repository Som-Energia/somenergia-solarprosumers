from rest_framework import viewsets

from somsolet_api.serializer import ProjectSerializer
from somsolet.models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.headers.get('dni')
        
        return Project.objects.filter(client__dni=user)
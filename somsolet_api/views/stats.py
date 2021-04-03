from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from somsolet.models import Campaign, Project
from somsolet_api.serializer import StatsSerializer


class StatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Campaign.objects.all()
    serializer_class = StatsSerializer
    
    def get_queryset(self):
        return Project.objects.filter(
            registration_date__isnull=False
        ).exclude(status='discarded')

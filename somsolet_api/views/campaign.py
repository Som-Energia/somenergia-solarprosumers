from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from somsolet.models import Campaign
from somsolet_api.serializer import CampaignSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Campaign.objects.all().order_by('name')
    serializer_class = CampaignSerializer

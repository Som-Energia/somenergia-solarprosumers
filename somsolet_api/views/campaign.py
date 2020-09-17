from rest_framework import viewsets

from somsolet_api.serializer import CampaignSerializer
from somsolet.models import Campaign


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('name')
    serializer_class = CampaignSerializer
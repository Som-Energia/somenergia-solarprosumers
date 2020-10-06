from rest_framework import viewsets
from somsolet.models import Campaign
from somsolet_api.serializer import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('name')
    serializer_class = CampaignSerializer

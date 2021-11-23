from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from somsolet.models import Campaign
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    serializer_class = CampaignSerializer

    def get_queryset(self):
        queryset = Campaign.objects.all().order_by('name')

        campaign = self.request.query_params.get('campaignId')
        if campaign:
            return queryset.filter(id=campaign)
        else:
            return queryset


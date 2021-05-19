from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from somsolet.models import Campaign
from somsolet_api.serializer import CampaignSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    queryset = Campaign.objects.all().order_by('name')
    serializer_class = CampaignSerializer
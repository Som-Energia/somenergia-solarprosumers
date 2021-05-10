from rest_framework import viewsets
from somsolet.models import Campaign
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import StatsSerializer


class StatsViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = StatsSerializer

    def get_queryset(self):
        queryset = Campaign.objects.all().order_by('name')

        campaign = self.request.query_params.get('campaignId')
        if campaign:
            return queryset.filter(id=campaign)
        else:
            return queryset

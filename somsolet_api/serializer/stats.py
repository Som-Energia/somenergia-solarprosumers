from rest_framework import serializers
from somsolet.models import Campaign, Project


class StatsSerializer(serializers.HyperlinkedModelSerializer):
    productionStats = serializers.SerializerMethodField('get_stats')

    class Meta:
        model = Campaign
        fields = (
            'productionStats',
        )

    def get_stats(self, campaign_obj):
        ongoing_installations = Project.objects.filter(
            campaign__name=campaign_obj.name,
            registration_date__isnull=False
        ).exclude(status='discarded').count()

        if ongoing_installations:
            return {
                'campaignId': campaign_obj.id,
                'totalInstalations': ongoing_installations,
                'totalPower': {
                    'value': ongoing_installations * 3,
                    'units': 'kWp'
                },
                'totalGeneration': {
                    'value': ongoing_installations * 3 * 1450 * 0.000001,
                    'units': 'GWp/any'
                }
            }
        return {}

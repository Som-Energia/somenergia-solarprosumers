from rest_framework import serializers
from somsolet.models import Campaign, Project


class StatsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='stats',
    )

    productionStats = serializers.SerializerMethodField('get_stats')

    class Meta:
        model = Campaign
        fields = (
            'url',
            'productionStats',
        )

    def get_stats(self, obj):

        ongoing_installations = Project.objects.filter(
            registration_date__isnull=False
        ).exclude(status='discarded').count()

        return {
            'total_instalations': ongoing_installations,
            'total_power': {
                'value': ongoing_installations * 3,
                'units': 'kWp'
            },
            'total_generation': {
                'value': ongoing_installations * 3 * 1450 * 0.000001,
                'units': 'GWp/any'
            }
        }

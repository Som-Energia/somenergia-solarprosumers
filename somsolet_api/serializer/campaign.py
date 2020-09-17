from rest_framework import serializers

from somsolet.models import Campaign, Project

from somsolet.choices_options import ITEM_COMMUNITY


class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    campaignId = serializers.CharField(source='id')
    dateStart = serializers.DateField(source='date_inscriptions_closed')
    dateEnd = serializers.DateField(source='date_completed_installations')
    engineerings = serializers.SerializerMethodField('get_engineerings')
    localGroups = serializers.SerializerMethodField('get_localGroups')
    region = serializers.SerializerMethodField('get_region')
    installationsStatus = serializers.SerializerMethodField('get_installations_status_summary')
    productionSummary = serializers.SerializerMethodField('get_production_summary')

    class Meta:
        model = Campaign
        fields = (
            'name', 
            'campaignId', 
            'dateStart', 'dateEnd', 
            'engineerings', 
            'localGroups', 
            'region',
            'installationsStatus',
            'productionSummary',
            )


    def get_engineerings(self, obj):
        return [
            {
                'name': e.name,
                'address': e.address,
                'email': e.email,
                'phoneNumber': e.phone_number,
            } for e in obj.engineerings.all()
            ]

    def get_localGroups(self, obj):
        return [
            {
                'name': lg.name,
                'email': lg.email,
            } for lg in obj.local_group.all()
            ]

    def get_region(self, obj):
        return {
            'autonomousCommunity': obj.get_autonomous_community_display(),
            'geographicalRegion': obj.geographical_region,
        }

    def get_installations_status_summary(self, obj):
        return {
            'foreseen': obj.count_foreseen_installations,
            'ongoing': Project.objects.filter(
                campaign__name=obj.name,
                registration_date__isnull=False
                ).exclude(status='discarded').count(),
            'completed': obj.count_completed_installations,
            'inscriptions':  Project.objects.filter(
                campaign__name=obj.name,
                registration_date__isnull=False
                ).count(),
        }

    def get_production_summary(self, obj):
        ongoing_installations =  Project.objects.filter(
                campaign__name=obj.name,
                registration_date__isnull=False
                ).exclude(status='discarded').count()
        return {
            'kWpInstalled': ongoing_installations * 3,
            'kWpPerYear': ongoing_installations * 1450,
            'GWhPerYear': ongoing_installations * 1450 * 0.000001,
            'GWhOverSom': ongoing_installations * 1450 * 0.000001 * 100 / 17.,
        }       
   

from rest_framework import serializers

from somsolet.models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    projectId = serializers.CharField(source='id')
    engineerings = serializers.SerializerMethodField('get_engineerings')

    class Meta:
        model = Project
        fields = (
            'name',
            'projectId',
            'engineerings', 
            )


    def get_engineerings(self, obj):
        return [
            {
                'name': e.name,
                'address': e.address,
                'email': e.email,
                'phoneNumber': e.phone_number,
            } for e in obj.campaign.engineerings.all()
            ]

from rest_framework import serializers
from somrenkonto.models import RenkontoEvent


class RenkontoEventSerializer(serializers.HyperlinkedModelSerializer):

    date_start = serializers.DateTimeField(
        source='start',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    date_end = serializers.DateTimeField(
        source='end',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    class Meta:
        model = RenkontoEvent
        fields = ('date_start', 'date_end', 'all_day')

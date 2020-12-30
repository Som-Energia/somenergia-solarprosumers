from rest_framework import serializers
from somrenkonto.models import RenkontoEvent


class RenkontoEventSerializer(serializers.HyperlinkedModelSerializer):

    date_start = serializers.DateTimeField()

    date_end = serializers.DateTimeField()

    class Meta:
        model = RenkontoEvent
        fields = ('date_start', 'date_end', 'all_day')
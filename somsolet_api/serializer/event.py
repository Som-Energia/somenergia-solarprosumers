from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from somrenkonto.models import RenkontoEvent, Calendar, EventChoices


class TechnicalVisitEventValues:

    _title = _('Technical event')
    _description = _('')
    _event_type = EventChoices.TECHNICAL_VISIT

    @classmethod
    def default_technical_visit_values(cls, **kwargs):
        return {
            'title': kwargs.get('title') or cls._title,
            'description': kwargs.get('description') or cls._description,
            'event_type': kwargs.get('event_type') or cls._event_type,
            'calendar': kwargs['calendar'],
            'project': kwargs['project'],
            'campaign': kwargs['project'].campaign
        }


class RenkontoEventSerializer(serializers.HyperlinkedModelSerializer):

    date_start = serializers.DateTimeField(
        source='start',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    date_end = serializers.DateTimeField(
        source='end',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    address = serializers.CharField(required=False)

    class Meta:
        model = RenkontoEvent
        fields = (
            'date_start', 'date_end', 'all_day', 'address',
            'event_type', 'project', 'campaign'
        )

    def to_representation(self, instance):
        return {
            'dateStart': instance.date_end,
            'dateEnd': instance.date_end,
            'allDay': instance.all_day,
            'eventType': instance.event_type,
            'address': instance.address,
            'installationId': instance.project,
            'campaignId': instance.campaign
        }

    def set_technical_visit(self, calendar, project):
        event_data = TechnicalVisitEventValues.default_technical_visit_values(
            calendar=calendar,
            project=project
        )
        return self.create({**event_data, **self.validated_data})
    
    def create(self, event_data):
        return RenkontoEvent.create(**event_data)
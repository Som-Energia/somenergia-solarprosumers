from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from schedule.models.calendars import Calendar
from somrenkonto.models import RenkontoEvent, EventChoices


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


class RenkontoEventSerializer(serializers.ModelSerializer):

    DATE_ERROR_MSG = _('Date end must occur after date start')
    CAMPAIGN_NOT_DEFINED_MSG = _('Campaign, project or both are not defined')

    class Meta:
        model = RenkontoEvent
        fields = (
            'title', 'description', 'date_start', 'date_end', 'all_day',
            'event_type', 'campaign', 'project', 'calendar', 'engineering'
        )

    date_start = serializers.DateTimeField(
        source='start',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    date_end = serializers.DateTimeField(
        source='end',
        format='%Y-%m-%dT%H:%M:%S%z'
    )

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError(self.DATE_ERROR_MSG)

        if data.get('project', False):
            campaign_defined = self._campaign_defined(
                data['engineering'], data['campaign'], data['project']
            )
            if not campaign_defined:
                raise serializers.ValidationError(self.CAMPAIGN_NOT_DEFINED_MSG)

        return data

    def _campaign_defined(self, engineering, campaign, project):
        return project.campaign.id == campaign.id \
            and project.engineering.id == engineering.id

    def set_technical_visit(self, calendar, project):
        event_data = TechnicalVisitEventValues.default_technical_visit_values(
            calendar=calendar, project=project
        )
        technical_visit = self.create(
            event_data={**event_data, **self.validated_data}
        )
        return technical_visit

    def create(self, event_data):
        return RenkontoEvent.create(
            title=event_data.get('title'),
            description=event_data.get('description'),
            start_date=event_data.get('start').date(),
            start_time=event_data.get('start').timetz(),
            end_date=event_data.get('end').date(),
            end_time=event_data.get('end').timetz(),
            all_day=event_data.get('all_day'),
            calendar=event_data.get('calendar').id,
            event_type=event_data.get('event_type'),
            campaing_name=event_data.get('campaign').name,
            installation_name=event_data.get('project').name,
        )

    def to_representation(self, instance):
        data = super(RenkontoEventSerializer, self).to_representation(instance)

        return {
            'dateStart': data.get('date_start'),
            'dateEnd': data.get('date_end'),
            'allDay': data.get('all_day'),
            'eventType': data.get('event_type'),
            'installationId': data.get('project'),
            'campaignId': data.get('campaign')
        }

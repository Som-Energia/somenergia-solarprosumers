import pytest
from django.urls import reverse
from django_currentuser.middleware import _set_current_user

from somrenkonto.models import RenkontoEvent, EventChoices
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.views import RenkontoEventView


class TestRenkontoEventSerializer:

    @pytest.mark.django_db
    def test__event_serializer(self, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)
        assert event_serializer.data == {
            'dateStart': bounded_event.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'dateEnd': bounded_event.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'allDay': bounded_event.all_day,
            'campaignId': bounded_event.campaign.id,
            'eventType': bounded_event.event_type,
            'installationId': bounded_event.project.id,
            'address': None
        }

    @pytest.mark.django_db
    def test__set_technical_visit(
        self, authenticated_user, technical_event, calendar, montse_project
    ):
        # given a technical_visit_event
        # a calendar
        # a project
        # and an authenticated user
        _set_current_user(authenticated_user)

        # when we set a new technical visit for that project
        event_serializer = RenkontoEventSerializer(
            data=technical_event, partial=True
        )
        event_serializer.is_valid()
        event = event_serializer.set_technical_visit(
            calendar=calendar,
            project=montse_project,
        )

        # then the event was created with the expected data
        created_event_serializer = RenkontoEventSerializer(
            instance=event,
            context={'request': None}
        )

        assert created_event_serializer.data == {
            'dateStart': technical_event.get('date_start'),
            'dateEnd': technical_event.get('date_end'),
            'allDay': technical_event.get('all_day') or False,
            'campaignId': montse_project.campaign.id,
            'eventType': EventChoices.TECHNICAL_VISIT,
            'installationId': montse_project.id,
            'address': None
        }

        # and has the given project and calendar
        assert event.project == montse_project
        assert event.calendar == calendar


@pytest.mark.django_db
class TestRenkontoEventView:

    def test__get_engineering_events(
        self, authenticated_user, engineering_with_events, rf,
    ):
        # given
        # an authenticated_user
        # an engineering with events

        # when the user requests for the events of an engineering
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.get(url)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, engineering_with_events.id)

        # then the user obtain a succesfull response and a list with the events of the engineering
        events = [
            RenkontoEventSerializer(event, context={'request': request}).data
            for event in RenkontoEvent.objects.filter(
                engineering__id=engineering_with_events.id
            )
        ]
        assert response.data == {
            'data': {
                'count': len(events),
                'results': events
            }
        }

    def test__get_engineering_events__enginieering_doesnotexists(
            self, authenticated_user, rf
    ):
        # given
        # an authenticated user
        unregistered_engineering_id = 4567

        # when the user requests for the events of that engineering
        url = reverse('events', args=[unregistered_engineering_id])
        request = rf.get(url)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, unregistered_engineering_id)

        # then the user obtain an empty response
        assert response.data == {
            'data': {
                'count': 0,
                'results': []
            }
        }

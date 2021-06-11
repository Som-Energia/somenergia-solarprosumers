import pytest
from django.urls import reverse

from somrenkonto.models import RenkontoEvent
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.views import RenkontoEventView


class TestRenkontoEventSerializer:

    @pytest.mark.django_db
    def test__event_serializer(self, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)

        assert event_serializer.data == {
            'date_start': bounded_event.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_end': bounded_event.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'all_day': bounded_event.all_day
        }

    @pytest.mark.django_db
    def test__set_technical_visit(self, technical_event, calendar, montse_project):
        # given a technical_visit_event
        # a calendar
        # and a project

        # when we set a new technical visit for that project
        event_serializer = RenkontoEventSerializer(data=technical_event)
        event_serializer.is_valid()

        event = event_serializer.set_technical_visit(calendar, montse_project)

        # then ???
        assert event_serializer.data == {}


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
            RenkontoEventSerializer(event).data
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

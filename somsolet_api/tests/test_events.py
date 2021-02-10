import pytest
from django.urls import reverse
from somrenkonto.models import RenkontoEvent
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.views import RenkontoEventView


class TestRenkontoEventSerializer:

    @pytest.mark.django_db
    def test_event_serializer(self, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)

        assert event_serializer.data == {
            'date_start': bounded_event.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_end': bounded_event.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'all_day': bounded_event.all_day
        }

class TestRenkontoEventView:

    @pytest.mark.django_db
    def test_get_engineering_events(
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

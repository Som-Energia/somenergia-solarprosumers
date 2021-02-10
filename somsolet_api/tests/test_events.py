import pytest
from somsolet_api.serializer import RenkontoEventSerializer


class TestEventSerializer:

    @pytest.mark.django_db
    def test_event_serializer(self, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)

        assert event_serializer.data == {
            'date_start': bounded_event.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_end': bounded_event.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'all_day': bounded_event.all_day
        }
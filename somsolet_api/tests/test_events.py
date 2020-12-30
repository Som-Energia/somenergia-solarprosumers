import pytest
from somsolet_api.serializer import RenkontoEventSerializer


class TestEvents:

    @pytest.mark.skip("TODO")
    def test_availability_engineering_hour(self, client):
        pass


class TestEventSerializer:

    @pytest.mark.django_db
    def test_event_serializer(self, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)

        assert event_serializer.data == {
            'start_date': bounded_event.start,
            'end_date': bounded_event.end,
            'all_day': bounded_event.all_day
        }
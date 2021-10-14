import pytest
from django.urls import reverse
from django_currentuser.middleware import _set_current_user

from somrenkonto.models import RenkontoEvent, EventChoices
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.views import RenkontoEventView
from .fixtures import authenticated_user


class TestRenkontoEventSerializer:

    @pytest.mark.django_db
    def test__event_serializer(self, authenticated_user, bounded_event):
        event_serializer = RenkontoEventSerializer(bounded_event)
        assert event_serializer.data == { 
            'dateStart': bounded_event.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'dateEnd': bounded_event.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'allDay': bounded_event.all_day,
            'campaignId': bounded_event.campaign.id,
            'eventType': bounded_event.event_type,
            'installationId': bounded_event.project.id
        }

    @pytest.mark.django_db
    def test__event_serializer__without_object(self, technical_visit_event_request):
        event_serializer = RenkontoEventSerializer(
            data=technical_visit_event_request,
            context={'request': None}
        )

        assert event_serializer.is_valid()
        assert event_serializer.data == {
            'dateStart': technical_visit_event_request['date_start'],
            'dateEnd': technical_visit_event_request['date_end'],
            'allDay': technical_visit_event_request['all_day'],
            'campaignId': technical_visit_event_request['campaign'],
            'eventType': technical_visit_event_request['event_type'],
            'installationId': technical_visit_event_request['project']
        }

    @pytest.mark.django_db
    def test__set_technical_visit(
        self, authenticated_user, technical_event, calendar, montse_project
    ):
        # given a technical_visit_event
        # a calendar
        # a project
        # and an authenticated user

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

    def test__post_engineering_events(
        self, authenticated_user, engineering_with_events, technical_visit_event_request, rf
    ):
        # given
        # an authenticated_user
        # an engineering with events
        # a new event data

        # when the user post that technical event data
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.post(url, technical_visit_event_request)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, engineering_with_events.id)

        # then the user obtain a succesfull response and the event was created 
        created_event = event = RenkontoEvent.objects.get(
            project_id=technical_visit_event_request['project'],
            title=technical_visit_event_request['title']
        )
        assert response.data == {
            'data': {
                'count': 1,
                'results': [created_event.id]
            }
        }

    def test__post_engineering_events__dates_error(
        self, authenticated_user, engineering_with_events, event_request_with_bad_dates, rf
    ):
        # given
        # an authenticated_user
        # an engineering with events
        # a new event data with incorrect dates

        # when the user post that technical event data
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.post(url, event_request_with_bad_dates)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, engineering_with_events.id)

        # then we have a 400 error
        assert response.status_code == 400

    def test__post_engineering_events__campaign_not_defined(
        self, authenticated_user, engineering_with_events, event_request_with_undefined_campaign, rf
    ):
        # given
        # an authenticated_user
        # an engineering with events
        # a new event data with a campaign that not exists

        # when the user post that technical event data
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.post(url, event_request_with_undefined_campaign)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, engineering_with_events.id)

        # then we have a 400 error
        assert response.status_code == 400

    def test__post_engineering_events__engineering_not_exists(
        self, authenticated_user, engineering_with_events, event_request_engineering_not_exists, rf
    ):
        # given
        # an authenticated_user
        # an engineering with events
        # a new event data

        # when the user post that technical event data
        url = reverse('events', args=[engineering_with_events.id])
        request = rf.post(url, event_request_engineering_not_exists)
        request.user = authenticated_user
        response = RenkontoEventView.as_view()(request, engineering_with_events.id)

        # then we have a 400 error
        assert response.status_code == 400

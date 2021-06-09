import pytest
from django.urls import reverse

from somsolet_api.views import SetTechnicalVisitView

from .factories import TechnicalVisitDataFactory


@pytest.mark.django_db
class TestProjectApi:

    def test__set_technical_visit__ok(authenticated_user, montse_project, rf):
        # given
        # an authenticated engineering
        # a project
        # and a valid set technical visit data
        techical_visit_data = TechnicalVisitDataFactory.data_ok

        # when that engineering sets a technical visit to a project
        url = reverse('set_technical_visit', args=[montse_project.id])
        request = rf.get(url)
        request.user = authenticated_user
        request.body = techical_visit_data
        response = SetTechnicalVisitView.as_view()(request, montse_project.id)

        # then the user obtain a successful response
        assert response.status_code == 200
        # and a summary of the event
        assert response.data == {
            'data': {
                'dateStart': '2020-06-12T10:20:50.52Z',
                'dateEnd': '2020-06-12T12:20:50.52Z',
                'allDay': False,
                'eventType': 'TECHNICAL_VISIT',
                'address': 'Carrer Belcaire 67',
                'installationId': 1,
                'campaignId': 3
            }
        }

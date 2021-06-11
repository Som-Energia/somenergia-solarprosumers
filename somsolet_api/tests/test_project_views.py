import pytest
from django.urls import reverse

from somsolet_api.views import ProjectViewSet

from .factories import TechnicalVisitDataFactory


@pytest.mark.django_db
class TestSetTechnicalVisitView:

    def test__set_technical_visit__ok(self, authenticated_user, montse_project, rf):
        # given
        # an authenticated engineering
        # a project
        # and a valid set technical visit data
        technical_visit_data = TechnicalVisitDataFactory.data_ok()

        # when that engineering sets a technical visit to a project
        url = reverse('project-set-technical-visit', args=[montse_project.id])
        request = rf.put(url, technical_visit_data, format='json')
        request.user = authenticated_user

        response = ProjectViewSet.as_view({
            'put': 'set_technical_visit'
        })(request, montse_project.id)

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

import pytest
from django.urls import reverse
from django_currentuser.middleware import _set_current_user

from somsolet_api.views import ProjectViewSet
from .factories import TechnicalVisitDataFactory


@pytest.mark.django_db
class TestSetTechnicalVisitView:

    def test__set_technical_visit__ok(self, authenticated_superuser, calendar, montse_project, rf):
        # given
        # an authenticated superuser
        _set_current_user(authenticated_superuser) 
        # a project
        # and a valid set technical visit data
        technical_visit_data = TechnicalVisitDataFactory.data_ok()

        # when that engineering sets a technical visit to a project
        url = reverse('project-set-technical-visit', args=[montse_project.id])
        request = rf.put(url, technical_visit_data, format='json')
        request.user = authenticated_superuser

        response = ProjectViewSet.as_view({
            'put': 'set_technical_visit'
        })(request, montse_project.id)

        # then the user obtain a successful response
        assert response.status_code == 200
        # and a summary of the event
        assert response.data == {
            'dateStart': technical_visit_data.get('date_start'),
            'dateEnd': technical_visit_data.get('date_end'),
            'allDay': False,
            'eventType': 'TECH',
            'address': None,
            'installationId': montse_project.id,
            'campaignId': montse_project.campaign_id
        }

    def test__set_technical_visit__without_permissions(self, authenticated_user, montse_project, calendar, rf):
        # given
        # an unauthenticated engineering
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

        # then the user can't acces to this resource
        assert response.status_code == 403


from django.urls import resolve, reverse


class TestUrls:

    def test_project_details_url(self):
        path = reverse('project', kwargs={'pk': 1})
        assert resolve(path).view_name == 'project'

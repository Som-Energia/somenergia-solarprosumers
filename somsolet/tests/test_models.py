import pytest

from somsolet.models import Project


@pytest.mark.django_db
class TestProjectModel:

    def test__technical_visit_dates(self, authenticated_user, technical_visit_event):
        # Given a project and technical visit event for that project
        # technical_visit_event.project
        # technical_visit_event
        project = technical_visit_event.project

        # when we look for that date in project
        technical_visit_dates = project.technical_visit_dates

        # then we have that technical visit event
        assert technical_visit_dates.count() == 1
        assert technical_visit_dates.first() == technical_visit_event


@pytest.mark.django_db
class TestProjectQuerySet:

    def test__get_project__ok(self, project, engineering_user_paco):
        # given a project
        # and an engineering that manage that project

        # if we search that project by id
        result = Project.projects.get_project(project.id, engineering_user_paco)

        # then we obtain the same project
        assert result == project

    def test__get_project__project_not_found(self, project, engineering_user):
        # given a project
        # and an engineering that doesn't manage that project

        # if we search that project by id
        result = Project.projects.get_project(project.id, engineering_user)

        # then we do not obtain any project
        assert result == None

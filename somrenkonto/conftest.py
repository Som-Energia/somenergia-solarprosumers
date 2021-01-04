import pytest

from . import factories


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():

        engineering_user = factories.UserFactory()
        engineering_user.save()
        
        calendar = factories.CalendarFactory()
        calendar.save()
        calendar.create_relation(engineering_user)

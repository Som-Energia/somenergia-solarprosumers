from datetime import datetime

import factory
import pytest
from factories import ProjectFactory
from scheduler_tasks import prereport_summary
from somsolet.models import Project


@pytest.mark.django_db
class TestSummaryReports:
    def test_prereport_with_no_overdue(self):
        ProjectFactory.create_batch(
            5,
            date_prereport=datetime.strptime("2020-01-01", "%Y-%m-%d"),
            name=factory.Sequence(lambda n: "TEST {0}".format(n)),
        )
        ProjectFactory.create_batch(
            10, name=factory.Sequence(lambda n: "TEST {0}".format(n))
        )
        summary = prereport_summary(Project.objects.filter(name__contains="TEST"))
        assert summary == [
            {"name": "Sent Prereports", "value": 5},
            {"name": "Unsent Prereports", "value": 10},
        ]

    def test_prereport_with_overdue(self):
        ProjectFactory.create_batch(
            5,
            date_prereport=datetime.strptime("2020-01-01", "%Y-%m-%d"),
            name=factory.Sequence(lambda n: "TEST {0}".format(n)),
        )
        ProjectFactory.create_batch(
            10, name=factory.Sequence(lambda n: "TEST {0}".format(n))
        )
        ProjectFactory.create_batch(
            2,
            warning="prereport",
            warning_date=datetime.strptime("2020-01-02", "%Y-%m-%d"),
            name=factory.Sequence(lambda n: "TEST {0}".format(n)),
        )
        summary = prereport_summary(Project.objects.filter(name__contains="TEST"))
        assert summary == [
            {"name": "Sent Prereports", "value": 5},
            {"name": "Unsent Prereports", "value": 12},
            {"name": "Overdue Prereports", "value": 2},
            {"name": "Maximum overdue days", "value": 103},
        ]

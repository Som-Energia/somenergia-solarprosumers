from datetime import date, datetime
from unittest import mock

import factory
import pytest

import scheduler_tasks
from somsolet.models import Project

from .factories import ProjectFactory


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
        summary = scheduler_tasks.prereport_summary(
            Project.objects.filter(name__contains="TEST")
        )
        assert summary == [
            {"name": "Sent Prereports", "value": 5},
            {"name": "Unsent Prereports", "value": 10},
        ]

    def test_prereport_with_overdue(self):

        with mock.patch("scheduler_tasks.date") as datetime_patcher:
            datetime_patcher.today.return_value = date(2020, 8, 3)

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
            summary = scheduler_tasks.prereport_summary(
                Project.objects.filter(name__contains="TEST")
            )
            assert summary == [
                {"name": "Sent Prereports", "value": 5},
                {"name": "Unsent Prereports", "value": 12},
                {"name": "Overdue Prereports", "value": 2},
                {"name": "Maximum overdue days", "value": 214},
            ]

from datetime import datetime

from parameterized import parameterized
from somsolet.forms import (
    ConstructionPermitForm,
    InstallationDateForm,
    OfferForm,
    PrereportForm,
    ReportForm,
    TechnicalVisitForm,
)


class TestForms:
    @parameterized.expand(
        [
            (
                datetime(2021, 12, 11),
                True,
                ("prereport review", datetime(2021, 12, 11), "No Warn"),
            ),
            (
                datetime(2021, 12, 11),
                False,
                ("prereport", datetime(2021, 12, 11), "No Warn"),
            ),
        ]
    )
    def test_prereportForm(self, date_prereport_review, is_invalid_prereport, expected):
        assert (
            PrereportForm.prereport(self, date_prereport_review, is_invalid_prereport)
            == expected
        )

    @parameterized.expand(
        [
            (
                datetime(2021, 12, 11),
                ("technical visit", datetime(2021, 12, 11), "No Warn"),
            ),
        ]
    )
    def test_technicalVisitForm(self, date_set_technical_visit, expected):
        assert (
            TechnicalVisitForm.set_technical_visit(
                self,
                date_set_technical_visit,
            )
            == expected
        )

    @parameterized.expand(
        [
            (
                datetime(2021, 12, 11),
                True,
                ("report review", datetime(2021, 12, 11), "No Warn"),
            ),
            (
                datetime(2021, 12, 11),
                False,
                ("report", datetime(2021, 12, 11), "No Warn"),
            ),
        ]
    )
    def test_reportForm(self, date_report_review, is_invalid_report, expected):
        assert (
            ReportForm.report(self, date_report_review, is_invalid_report) == expected
        )

    @parameterized.expand(
        [
            (
                datetime(2021, 12, 11),
                True,
                ("offer review", datetime(2021, 12, 11), "No Warn"),
            ),
            (
                datetime(2021, 12, 11),
                False,
                ("offer", datetime(2021, 12, 11), "No Warn"),
            ),
        ]
    )
    def test_offerForm(self, date_upload_offer, is_invalid_offer, expected):
        assert OfferForm.offer(self, date_upload_offer, is_invalid_offer) == expected

    @parameterized.expand(
        [
            (datetime(2021, 12, 11), ("construction permit", "No Warn")),
            ("", ("signature", "No Warn")),
        ]
    )
    def test_constructionPermitForm(self, date_permit, expected):
        assert (
            ConstructionPermitForm.construction_permit(
                self,
                date_permit,
            )
            == expected
        )

    @parameterized.expand(
        [
            (datetime(2021, 12, 11), ("date installation set", True, "No Warn")),
            ("", ("pending installation date", False, "installation date")),
        ]
    )
    def test_installationDateForm(self, date_installation, expected):
        assert (
            InstallationDateForm.set_date_installation(
                self,
                date_installation,
            )
            == expected
        )

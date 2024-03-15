import django_tables2 as tables
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_tables2.utils import A

from .models import Campaign, Project


class CampaignTable(tables.Table):
    name = tables.LinkColumn(
        "project",
        args=[A("pk")],
        verbose_name=_("Campaign"),
    )

    technical_campaign = tables.TemplateColumn(
        template_name="somsolet/technical_campaign_update.html",
        verbose_name=_("Technical Details"),
    )

    calendar = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name=_("Calendar"),
    )

    class Meta:
        model = Campaign
        fields = ["name", "active"]

    def render_calendar(self, record):
        base_url = reverse("somrenkonto")
        url = f"{base_url}?campaign_id={record.id}"
        link_title = _("Show Calendar")
        return format_html(f"<a href={url}>{link_title}</a>")


class ProjectTable(tables.Table):
    client = tables.LinkColumn(
        "client",
        args=[A("client_id")],
        accessor="client.name",
    )

    upload_prereport = tables.LinkColumn(
        "prereport",
        args=[A("pk")],
        verbose_name=_("Prereport"),
    )

    date_technical_visit = tables.TemplateColumn(
        template_name="somsolet/date_technical_visit_column.html",
    )

    upload_report = tables.LinkColumn("report", args=[A("pk")])

    upload_offer = tables.LinkColumn("offer", args=[A("pk")])

    upload_contract = tables.LinkColumn("signed_contract", args=[A("pk")])

    upload_permit = tables.LinkColumn("construction_permit", args=[A("pk")])

    date_start_installation = tables.TemplateColumn(
        template_name="somsolet/date_start_installation_column.html",
    )

    upload_delivery_certificate = tables.LinkColumn(
        "delivery_certificate", args=[A("pk")]
    )

    upload_legal_docs = tables.LinkColumn("legalization", args=[A("pk")])

    upload_legal_registration_docs = tables.LinkColumn(
        "legal_registration", args=[A("pk")]
    )

    technical_details = tables.TemplateColumn(
        template_name="somsolet/technical_details_update.html",
        verbose_name=_("Technical Details"),
    )

    download_cch = tables.TemplateColumn(
        template_name="somsolet/download_cch.html",
        verbose_name=_("Download CCH"),
        orderable=False,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "client",
            "status",
            "warning",
            "date_prereport",
            "is_invalid_prereport",
            "upload_prereport",
            "date_technical_visit",
            "date_report",
            "is_invalid_report",
            "upload_report",
            "date_offer",
            "is_invalid_offer",
            "upload_offer",
            "date_signature",
            "upload_contract",
            "date_permit",
            "upload_permit",
            "date_start_installation",
            "date_delivery_certificate",
            "upload_delivery_certificate",
            "date_legal_registration_docs",
            "upload_legal_registration_docs",
            "date_legal_docs",
            "upload_legal_docs",
        ]

    def render_status(self, value):
        return format_html(
            '<span class="status {}">\
            <i class="fa fa-circle" title="{}" aria-hidden="true">\
            </i></span>',
            slugify(value),
            value,
        )

    def render_upload_prereport(self, value):
        if value.name != "uploaded_files/prereport/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_report(self, value):
        if value.name != "uploaded_files/report/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_offer(self, value):
        if value.name != "uploaded_files/offer/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_contract(self, value):
        if value.name != "uploaded_files/contract/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_permit(self, value):
        if value.name != "uploaded_files/permit/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_delivery_certificate(self, value):
        if value.name != "uploaded_files/delivery_certificate/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_legal_docs(self, value):
        if value.name != "uploaded_files/legal_docs/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

    def render_upload_legal_registration_docs(self, value):
        if value.name != "uploaded_files/legal_registration_docs/som.png":
            return format_html('<i class="fa fa-file" title="{}"/>', value.name)
        else:
            return format_html('<i class="fa fa-upload"')

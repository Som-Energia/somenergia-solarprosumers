import django_tables2 as tables
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from django_tables2.utils import A

from .models import Campaign, Project


class CampaignTable(tables.Table):
    name = tables.LinkColumn(
        'project',
        args=[A('pk')],
        verbose_name='Campaign',)
    technical_campaign = tables.TemplateColumn(
        template_name='somsolet/technical_campaign_update.html',
        extra_context={'record': A('pk'), 'technical_campaign': A('pk')},
        verbose_name='Technical Details',)

    class Meta:
        model = Campaign
        fields = [
            'name',
            'active'
        ]


class ProjectTable(tables.Table):

    client = tables.LinkColumn(
        'client',
        args=[A('client_id')],
        accessor='client.name',)
    upload_prereport = tables.LinkColumn(
        'prereport',
        args=[A('pk')],
        verbose_name='Prereport',)
    date_technical_visit = tables.TemplateColumn(
        template_name='somsolet/date_technical_visit_column.html',
        extra_context={'record': A('pk'), 'date_technical_visit': A('pk')},)
    upload_report = tables.LinkColumn(
        'report',
        args=[A('pk')])
    upload_offer = tables.LinkColumn(
        'offer',
        args=[A('pk')])
    upload_permit = tables.LinkColumn(
        'construction_permit',
        args=[A('pk')])
    date_start_installation = tables.TemplateColumn(
        template_name='somsolet/date_start_installation_column.html',
        extra_context={'record': A('pk'), 'date_start_installation': A('pk')},)
    technical_details = tables.TemplateColumn(
        template_name='somsolet/technical_details_update.html',
        extra_context={'record': A('pk'), 'technical_details': A('pk')},
        verbose_name='Technical Details',)

    class Meta:
        model = Project
        fields = [
            'name',
            'client',
            'status',
            'warning',
            'date_prereport',
            'is_invalid_prereport',
            'upload_prereport',
            'date_technical_visit',
            'date_report',
            'is_invalid_report',
            'upload_report',
            'date_offer',
            'is_invalid_offer',
            'upload_offer',
            'date_permit',
            'upload_permit',
            'date_start_installation',
        ]

    def render_status(self, value):
        return format_html("<span class=\"status {}\"><i class=\"fa fa-circle\" title=\"{}\" aria-hidden=\"true\"></i></span>", slugify(value), value)

    def render_upload_prereport(self, value):
        if value.name != 'uploaded_files/som.png':
            return format_html("<i class=\"fa fa-file\" title=\"{}\"/>", value.name)
        else:
            return format_html("<i class=\"fa fa-times\"")

    def render_upload_report(self, value):
        if value.name != 'uploaded_files/som.png':
            return format_html("<i class=\"fa fa-file\" title=\"{}\"/>", value.name)
        else:
            return format_html("<i class=\"fa fa-times\"")

    def render_upload_offer(self, value):
        if value.name != 'uploaded_files/som.png':
            return format_html("<i class=\"fa fa-file\" title=\"{}\"/>", value.name)
        else:
            return format_html("<i class=\"fa fa-times\"")

    def render_upload_permit(self, value):
        if value.name != 'uploaded_files/som.png':
            return format_html("<i class=\"fa fa-file\" title=\"{}\"/>", value.name)
        else:
            return format_html("<i class=\"fa fa-times\"")

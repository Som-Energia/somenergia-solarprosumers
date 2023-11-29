import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Campaign, Project
from .models.choices_options import ITEM_WARNINGS, ProjectStatus


class ProjectListFilter(django_filters.FilterSet):

    client = django_filters.CharFilter(
        field_name="client__name", lookup_expr="icontains"
    )
    status = django_filters.ChoiceFilter(
        choices=ProjectStatus.choices,
        empty_label=_("--- Status ---"),
    )
    warning = django_filters.ChoiceFilter(
        choices=ITEM_WARNINGS,
        empty_label=_("--- Warning ---"),
    )
    municipality = django_filters.CharFilter(
        field_name="technical_details__municipality", lookup_expr="icontains"
    )
    administrative_division = django_filters.CharFilter(
        field_name="technical_details__administrative_division", lookup_expr="icontains"
    )

    class Meta:
        model = Project
        fields = []


class CampaignListFilter(django_filters.FilterSet):
    class Meta:
        model = Campaign
        fields = []

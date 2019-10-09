import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Project, Campaign
from .choices_options import ITEM_STATUS, ITEM_WARNINGS


class ProjectListFilter(django_filters.FilterSet):

    client = django_filters.CharFilter(
        field_name='client__name',
        lookup_expr='icontains'
    )
    status = django_filters.ChoiceFilter(
        choices=ITEM_STATUS,
        empty_label=_('--- Status ---'),
    )
    warning = django_filters.ChoiceFilter(
        choices=ITEM_WARNINGS,
        empty_label=_('--- Warning ---'),
    )

    class Meta:
        model = Project
        fields = []


class CampaignListFilter(django_filters.FilterSet):

    class Meta:
        model = Campaign
        fields = []

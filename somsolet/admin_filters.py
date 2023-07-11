from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Campaign


class CampaignNameListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Campaign')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'campaign__id__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (campaign.id, campaign.name)
            for campaign in Campaign.objects.all().order_by("name")
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(campaign__pk=self.value())

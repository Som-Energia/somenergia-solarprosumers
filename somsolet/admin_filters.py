from admin_auto_filters.filters import AutocompleteFilter


class CampaignNameListFilter(AutocompleteFilter):
    title = "Campaign"
    field_name = "campaign"

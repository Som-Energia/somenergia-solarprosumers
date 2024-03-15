from django.db import models
from django.utils.translation import gettext_lazy as _

from .admin import Engineering, LocalGroup
from .choices_options import ITEM_COMMUNITY


class CampaignQuerySet(models.QuerySet):
    def user_campaigns(self, user):
        user_campaigns_query = models.Q(engineerings=Engineering.objects.get(user=user))
        return self.filter(user_campaigns_query)


class Campaign(models.Model):
    name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_("Name"),
    )

    engineerings = models.ManyToManyField(
        Engineering, related_name="campaigns", verbose_name=_("Engineering")
    )

    local_group = models.ManyToManyField(
        LocalGroup, related_name="campaigns", verbose_name=_("LocalGroup")
    )

    date_call_for_engineerings = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date call for engineerings"),
    )

    date_call_for_inscriptions = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("date call for inscriptions"),
    )

    date_inscriptions_closed = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date inscriptions closed"),
    )

    date_completed_installations = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date completed installations"),
    )

    autonomous_community = models.CharField(
        choices=ITEM_COMMUNITY,
        default="empty",
        max_length=50,
        verbose_name=_("Autonomous community"),
    )

    geographical_region = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Geographical region"),
    )

    count_foreseen_installations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Number of planned installations"),
    )

    count_completed_installations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Count completed installations"),
    )

    kwp_installed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("kWp installed"),
    )

    date_warranty_payment = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date warranty payment"),
    )

    warranty_pending_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Pending Warranty (€)"),
    )

    warranty_payed_amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Payed Warranty (€)"),
    )

    total_penalties_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Total Penalties (days)"),
    )

    total_amount_penalties = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Total Penalties (€)"),
    )

    active = models.BooleanField(default=True)

    notify = models.BooleanField(default=True)

    objects = models.Manager()

    campaigns = CampaignQuerySet.as_manager()

    def __str__(self):
        return self.name


class Technical_campaign(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        verbose_name=_("Campaign"),
    )

    price_mono_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Monofasic Fixed Price (€)"),
    )

    price_mono_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Monofasic Variable Price (€/Wp)"),
    )

    price_tri_fixed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Trifasic Fixed Price (€)"),
    )

    price_tri_var = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Trifasic Variable Price (€/Wp)"),
    )

    def __str__(self):
        return self.campaign.name

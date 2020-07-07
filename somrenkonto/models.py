from django.db import models

from schedule.models import Event

from somsolet.models import Campaign, Project


class RenkontoEvent(Event):

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

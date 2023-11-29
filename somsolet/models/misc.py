from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices_options import ITEM_STATUS
from .project import Project


class Mailing(models.Model):
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Project"),
    )

    notification_status = models.CharField(
        choices=ITEM_STATUS, default=_("empty status"), max_length=50
    )

    sent = models.BooleanField(
        default=False, verbose_name=_("Sent"), help_text=_("True if an email was sent")
    )

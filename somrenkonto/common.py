from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Base(models.Model):

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name=_('created_by'),
        help_text=_('who created this object')
    )

    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='modified_events',
        verbose_name=_('created_by'),
        help_text=_('who modified this object')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
        help_text=_('when was created this object')
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('created_by'),
        help_text=_('last update of this object')
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('created_by'),
        help_text=_('when was deleted this object')
    )

    class Meta:
        abstract = True
    

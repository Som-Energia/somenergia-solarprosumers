from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user

class Base(models.Model):

    class Meta:
        abstract = True

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_created',
        verbose_name=_('created_by'),
        help_text=_('who created this object')
    )

    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_modified',
        verbose_name=_('modified_by'),
        help_text=_('who modified this object')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
        help_text=_('when was created this object')
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at'),
        help_text=_('last time this object updated')
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('deleted at'),
        help_text=_('when was deleted this object')
    )

    def save(self, *args, **kwargs):
        current_user = get_current_authenticated_user()
        if not self.id:
            self.created_by = current_user
        self.modified_by = current_user
        super().save(*args, **kwargs)

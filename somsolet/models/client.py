from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices_options import (BATERY_BRAND, INVERSOR_BRAND, ITEM_ANGLES,
                              ITEM_COMMUNITY, ITEM_DISCARDED_TYPES,
                              ITEM_ORIENTATION, ITEM_STATUS, ITEM_WARNINGS,
                              LANGUAGES, PANELS_BRAND, PANELS_TYPE)

class ClientFile(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Filename'),
    )

    file = models.FileField(
        upload_to='uploaded_files_som/general_conditions',
        null=True,
        blank=True,
        verbose_name=_('Upload general conditions')
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language')
    )

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Name'),
    )

    membership_number = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Membership number'),
    )

    dni = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('DNI'),
    )

    phone_number = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Telephone number'),
    )

    email = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Email'),
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language'),
    )

    sent_general_conditions = models.BooleanField(
        default=False,
        verbose_name=_('General conditions sent')
    )

    file = models.ManyToManyField(
        ClientFile,
        related_name='clients',
        verbose_name=_('File')
    )

    def __str__(self):
        return self.name

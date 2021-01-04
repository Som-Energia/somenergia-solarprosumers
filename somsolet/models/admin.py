from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices_options import LANGUAGES


class LocalGroup(models.Model):
    name = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Name'),
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

    def __str__(self):
        return self.name


class Engineering(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('User'),
    )

    name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Name'),
    )

    tin = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Tax identification number'),
    )

    address = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Address'),
    )

    email = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Email'),
    )

    phone_number = models.CharField(
        blank=True,
        max_length=9,
        verbose_name=_('Telephone number'),
    )

    count_closed_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Campaigns'),
    )

    count_open_campaigns = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Open Campaigns'),
    )

    count_closed_projects = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Closed Installations'),
    )

    total_kwp_installed = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Total kWp installed'),
    )

    comments = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('Comments'),
    )

    language = models.CharField(
        default='ca',
        choices=LANGUAGES,
        max_length=5,
        verbose_name=_('Language'),
    )

    def __str__(self):
        return self.name

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices_options import LANGUAGES


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

    # To Do: remove after migrate notification address
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
        verbose_name=_('General conditions File')
    )

    def __str__(self):
        return self.name


class NotificationAddress(models.Model):
    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notification_address',
        related_query_name='notification_address',
        verbose_name=_('Client'),
        help_text=_('Client associated with this address')
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



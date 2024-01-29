import logging

from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget

from somsolet.admin_filters import CampaignNameListFilter, EngineeringNameListFilter
from somsolet.tasks import send_registration_email

from .models import (
    Campaign,
    Client,
    ClientFile,
    Engineering,
    LocalGroup,
    Project,
    Technical_campaign,
    Technical_details,
)

logger = logging.getLogger("admin")


class ProjectResource(resources.ModelResource):
    name = fields.Field(attribute="name", column_name="Codi Instal·lació")
    campaign = fields.Field(
        attribute="campaign",
        column_name="campanya",
        widget=ForeignKeyWidget(Campaign, "name"),
    )
    client = fields.Field(
        attribute="client",
        column_name="Número de soci/a de Som Energia",
        widget=ForeignKeyWidget(Client, "membership_number"),
    )
    registration_date = fields.Field(
        attribute="registration_date",
        column_name="Data pagament 150 euros",
        widget=DateWidget('%d/%m/%Y')
    )

    class Meta:
        model = Project
        import_id_fields = ("name", "campaign", "client", "registration_date")
        exclude = ("id")

    def before_import_row(self, row, row_number=None, **kwargs):
        raw_client = self._get_client_from_row(row)
        client, created = Client.objects.get_or_create(
            email=raw_client["email"], dni=raw_client["dni"], defaults=raw_client
        )
        if created:
            logger.info("Client with email %s has been created", client.email)

    def after_save_instance(self, instance, using_transactions=True, dry_run=False):
        if not dry_run and not instance.registration_email_sent:
            send_registration_email.delay(project=instance)
            instance.status = "registered"
            instance.is_paid = True
            instance.save()

    def after_import_row(self, row, row_result, row_number, **kwargs):
        raw_technical_details = self._get_technical_details_from_row(row)
        instance = Project.objects.get(pk=row_result.object_id)
        Technical_details.objects.get_or_create(
            project=instance,
            campaign=instance.campaign,
            client=instance.client,
            defaults=raw_technical_details,
        )

    def _get_client_from_row(self, import_row):
        return {
            "name": import_row.get("Nom i cognoms", ""),
            "membership_number": import_row.get("Número de soci/a de Som Energia", ""),
            "dni": import_row.get("Número de DNI", ""),
            "phone_number": import_row.get("Telèfon de contacte", ""),
            "email": import_row.get("Correu electrònic", ""),
            "language": import_row.get("Idioma", settings.LANGUAGE_CODE_CA)
            or settings.LANGUAGE_CODE_CA,
        }

    def _get_technical_details_from_row(self, import_row):
        return {
            "administrative_division": import_row.get("Comarca", ""),
            "municipality": import_row.get("Municipi", ""),
            "street": import_row.get("Adreça", ""),
            "contract_number": import_row.get(
                "Número de contracte amb Som Energia", ""
            ),
            "cups": import_row.get(
                "CUPS - Codi Unificat del Punt de Subministrament", ""
            ),
            "voltage": import_row.get("Tipus d'instal·lació", ""),
            "tariff": import_row.get("Tarifa d'accès", ""),
            "anual_consumption": import_row.get(
                "Selecciona l'ús anual d'electricitat d'aquest habitatge o local"
            ),
            "installation_singlephase_model": import_row.get("Model monofàsic triat"),
            "installation_threephase_model": import_row.get("Model trifàsic triat"),
            "acquire_interest": import_row.get("Estic interessat en adquirir"),
            "client_comments": import_row.get("COMENTARIOS", ""),
        }


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ("campaign", "name", "client", "status", "warning", "warning_date")
    list_filter = (CampaignNameListFilter, "status", "discarded_type", "warning")
    search_fields = ("name", "status", "client__name")
    exclude = ["preregistration_date"]
    resource_class = ProjectResource


@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin):
    list_display = ("name", "autonomous_community", "date_warranty_payment", "notify")
    list_editable = ["notify"]
    list_filter = (EngineeringNameListFilter, "autonomous_community")
    search_fields = ("name", "autonomous_community")


@admin.register(Technical_campaign)
class Technical_CampaignAdmin(ImportExportModelAdmin):
    pass


@admin.register(Engineering)
class EngineeringAdmin(ImportExportModelAdmin):
    list_display = ("name", "phone_number", "email")
    search_fields = ("name", "phone_number", "email")


class Technical_detailsResource(resources.ModelResource):
    project = fields.Field(
        attribute="project",
        column_name="Codi Instal·lació",
        widget=ForeignKeyWidget(Project, "name"),
    )
    campaign = fields.Field(
        attribute="campaign",
        column_name="campanya",
        widget=ForeignKeyWidget(Campaign, "name"),
    )
    client = fields.Field(
        attribute="client",
        column_name="Número de DNI",
        widget=ForeignKeyWidget(Client, "dni"),
    )
    administrative_division = fields.Field(
        attribute="administrative_division", column_name="Comarca"
    )
    municipality = fields.Field(attribute="municipality", column_name="Municipi")
    street = fields.Field(attribute="street", column_name="Adreça")
    contract_number = fields.Field(
        attribute="contract_number", column_name="Número de contracte amb Som Energia"
    )
    cups = fields.Field(
        attribute="cups", column_name="CUPS - Codi Unificat del Punt de Subministrament"
    )
    voltage = fields.Field(attribute="voltage", column_name="Tipus d'instal·lació")
    tariff = fields.Field(attribute="tariff", column_name="Tarifa d'accès")
    anual_consumption = fields.Field(
        attribute="anual_consumption",
        column_name=(
            "Selecciona l'ús anual d'electricitat d'aquest" " habitatge o local"
        ),
    )
    installation_singlephase_model = fields.Field(
        attribute="installation_singlephase_model", column_name="Model monofàsic triat"
    )
    installation_threephase_model = fields.Field(
        attribute="installation_threephase_model", column_name="Model trifàsic triat"
    )
    acquire_interest = fields.Field(
        attribute="acquire_interest", column_name="Estic interessat en adquirir"
    )
    client_comments = fields.Field(
        attribute="client_comments", column_name="COMENTARIOS"
    )

    class Meta:
        model = Technical_details
        import_id_fields = ("project", "campaign", "client")
        exclude = ("id",)


@admin.register(Technical_details)
class Technical_detailsAdmin(ImportExportModelAdmin):
    list_display = ("campaign", "project", "client")
    list_filter = ("campaign", "client")
    resource_class = Technical_detailsResource


class ClientResource(resources.ModelResource):
    name = fields.Field(attribute="name", column_name="Nom i cognoms")
    membership_number = fields.Field(
        attribute="membership_number", column_name="Número de soci/a de Som Energia"
    )
    dni = fields.Field(attribute="dni", column_name="Número de DNI")
    phone_number = fields.Field(
        attribute="phone_number", column_name="Telèfon de contacte"
    )
    email = fields.Field(attribute="email", column_name="Correu electrònic")
    language = fields.Field(attribute="language", column_name="Idioma")

    class Meta:
        model = Client
        import_id_fields = ("name", "membership_number", "dni")
        exclude = ("id", "sent_general_conditions", "file")

    def before_import_row(self, row, **kwargs):
        row["Nom i cognoms"] = row["Nom i cognoms"].title()
        row["Número de DNI"] = row["Número de DNI"].upper()


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    list_display = ("name", "membership_number", "email")
    resource_class = ClientResource
    search_fields = ["name", "email", "membership_number"]


@admin.register(ClientFile)
class ClientFileAdmin(admin.ModelAdmin):
    list_display = ("name", "language")


@admin.register(LocalGroup)
class LocalGroupAdmin(ImportExportModelAdmin):
    list_display = ("name", "phone_number", "email")
    search_fields = ["name", "email"]

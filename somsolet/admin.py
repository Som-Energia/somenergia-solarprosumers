from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from .models import (Campaign, Client, Engineering, Project,
                     Technical_campaign, Technical_details)


class ProjectResource(resources.ModelResource):
    name = fields.Field(
        attribute='name',
        column_name='instalació')
    campaign = fields.Field(
        attribute='campaign',
        column_name="campanya",
        widget=ForeignKeyWidget(Campaign, 'name'))
    client = fields.Field(
        attribute='client',
        column_name="Número de soci/a de Som Energia",
        widget=ForeignKeyWidget(Client, 'membership_number'))

    class Meta:
        model = Project
        import_id_fields = ('name', 'campaign', 'client')
        exclude = ('id', )


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('campaign', 'client', 'status', 'warning')
    list_filter = ('campaign', 'status', 'discarded_type')
    resource_class = ProjectResource


class InstallationsInline(admin.TabularInline):
    model = Project


@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'engineering',
        'autonomous_community',
        'date_warranty_payment'
    )
    list_filter = (
        'engineering',
        'autonomous_community'
    )
    inlines = [InstallationsInline]


@admin.register(Technical_campaign)
class Technical_CampaignAdmin(ImportExportModelAdmin):
    pass


@admin.register(Engineering)
class EngineeringAdmin(ImportExportModelAdmin):
    list_display = ('name', 'phone_number', 'email')


class Technical_detailsResource(resources.ModelResource):
    project = fields.Field(
        attribute='project',
        column_name="instalació",
        widget=ForeignKeyWidget(Project, 'name'))
    campaign = fields.Field(
        attribute='campaign',
        column_name="campanya",
        widget=ForeignKeyWidget(Campaign, 'name'))
    client = fields.Field(
        attribute='client',
        column_name="Número de DNI",
        widget=ForeignKeyWidget(Client, 'dni'))
    administrative_division = fields.Field(
        attribute='administrative_division',
        column_name="Comarca")
    municipality = fields.Field(
        attribute='municipality',
        column_name="Municipi")
    street = fields.Field(
        attribute='street',
        column_name="Adreça")
    contract_number = fields.Field(
        attribute='contract_number',
        column_name="Número de contracte amb Som Energia")
    cups = fields.Field(
        attribute='cups',
        column_name="CUPS - Codi Unificat del Punt de Subministrament")
    voltage = fields.Field(
        attribute='voltage',
        column_name="Tipus d'instal·lació")
    tariff = fields.Field(
        attribute='tariff',
        column_name="Tarifa d'accès")
    anual_consumption = fields.Field(
        attribute='anual_consumption',
        column_name="Selecciona l'ús anual d'electricitat d'aquest habitatge o local")
    installation_singlephase_model = fields.Field(
        attribute='installation_singlephase_model',
        column_name="Model monofàsic triat")
    installation_threephase_model = fields.Field(
        attribute='installation_threephase_model',
        column_name="Model trifàsic triat")
    acquire_interest = fields.Field(
        attribute='acquire_interest',
        column_name="Estic interessat en adquirir")
    comments = fields.Field(
        attribute='comments',
        column_name="COMENTARIOS")

    class Meta:
        model = Technical_details
        import_id_fields = ('project', 'campaign', 'client')
        exclude = ('id', )


@admin.register(Technical_details)
class Technical_detailsAdmin(ImportExportModelAdmin):
    list_display = ('campaign', 'project', 'client')
    list_filter = ('campaign', 'client')
    resource_class = Technical_detailsResource


class ClientResource(resources.ModelResource):
    name = fields.Field(
        attribute='name',
        column_name='Nom i cognoms')
    membership_number = fields.Field(
        attribute='membership_number',
        column_name='Número de soci/a de Som Energia')
    dni = fields.Field(
        attribute='dni',
        column_name='Número de DNI')
    phone_number = fields.Field(
        attribute='phone_number',
        column_name='Telèfon de contacte')
    email = fields.Field(
        attribute='email',
        column_name='Correu electrònic')

    class Meta:
        model = Client
        import_id_fields = ('name', 'membership_number', 'dni')
        exclude = ('id', )


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    list_display = ('name', 'membership_number', 'email')
    resource_class = ClientResource

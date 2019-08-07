from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Project, Campaign, Client, Technical_details, Engineering

#admin.site.register(Project)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'client', 'status', 'warning')
    list_filter = ('campaign','status', 'discarded_type')


    fieldsets = (
        (None, {
            'fields': ('campaign', 'status')
        }),
        ('Execution details', {
            'fields': ('is_invalid_report', 'is_signed') #just for testing... add relevant fields
            #'fields': ('date_start_installation', 'engineering')
        }),
    )

class CampaignInline(admin.TabularInline):
    model = Project

@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin):
    list_display = ('name', 'engineering', 'autonomous_community', 'date_warranty_payment')
    list_filter = ('engineering', 'autonomous_community')
    inlines = [CampaignInline]


@admin.register(Technical_campaign)
class Technical_CampaignAdmin(ImportExportModelAdmin):
    pass


@admin.register(Engineering)
class EngineeringAdmin(ImportExportModelAdmin):
    pass


class Technical_detailsResource(resources.ModelResource):
    comments = fields.Field(attribute='comments', column_name='COMENTARIOS')

    class Meta:
        model = Technical_details


@admin.register(Technical_details)
class Technical_detailsAdmin(ImportExportModelAdmin):
    resource_class = Technical_detailsResource


class ClientResource(resources.ModelResource):
    name = fields.Field(
        attribute='name',
        column_name='Nombre y apellidos')
    membership_number = fields.Field(
        attribute='membership_number',
        column_name='Número de socio/a de Som Energia')
    dni = fields.Field(
        attribute='dni',
        column_name='Número de DNI')
    phone_number = fields.Field(
        attribute='phone_number',
        column_name='Teléfono de contacto')
    email = fields.Field(
        attribute='email',
        column_name='Correo electrónico')

    class Meta:
        model = Client


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource

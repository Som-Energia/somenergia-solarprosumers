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


@admin.register(Technical_details)
class Technical_detailsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    pass


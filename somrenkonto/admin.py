from django.contrib import admin
from django.forms.widgets import Input
from django.forms import ModelForm

from .models import CalendarConfig, RenkontoEvent


class ColorInput(Input):
    input_type = "color"


class EventAdminForm(ModelForm):
    class Meta:
        exclude = []
        model = RenkontoEvent
        widgets = {"color_event": ColorInput}


@admin.register(RenkontoEvent)
class RenkontoEventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("title", "color_event"),
                    ("description",),
                    ("start", "end"),
                    ("creator", "calendar"),
                    ("rule", "end_recurring_period"),
                ]
            },
        ),
        (
            'Campaign',
            {
                "fields": [
                    ("campaign",),
                ]
            },
        ),
        (
            'Project',
            {
                "fields": [
                    ("project",),
                ]
            },
        ),
        (
            'Meta',
            {
                "fields": [
                    ("created_by", "modified_by"),
                    ("created_at"),
                    ("modified_at"),
                    ("deleted_at"),
                ]
            }
        ),
    )

    readonly_fields = ("created_at", "modified_at")

    form = EventAdminForm

@admin.register(CalendarConfig)
class CalendarConfigAdmin(admin.ModelAdmin):
    pass
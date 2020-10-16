from django.contrib import admin
from django.forms.widgets import Input
from django.forms import ModelForm

from .models import RenkontoEvent


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
    )
    form = EventAdminForm
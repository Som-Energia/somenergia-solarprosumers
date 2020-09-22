from django import forms
from django.utils.translation import gettext_lazy as _


class CalendarForm(forms.Form):

    name = forms.CharField(
        max_length=256,
        required=True,
        help_text=_('Name of the calendar')
    )

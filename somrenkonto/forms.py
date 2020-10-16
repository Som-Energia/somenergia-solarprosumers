from django import forms
from django.utils.translation import gettext_lazy as _


class CalendarForm(forms.Form):

    name = forms.CharField(
        max_length=256,
        required=True,
        help_text=_('Name of the calendar')
    )


class EventFormChoices(object):

    APPOINTMENT = 'APPO'

    UNAVAILABILITY = 'UNAVAIL'

    AVAILABILITY = 'AVAIL'

    choices = [
        (APPOINTMENT, _('Appointment')),
        (UNAVAILABILITY, _('Unavailability')),
        (AVAILABILITY, _('Availability hours'))
    ]


class EventForm(forms.Form):

    title = forms.CharField(
        max_length=256,
        required=True,
        help_text=_('Tittle of the event')
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text=_('Description of the event')
    )

    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'id': 'initial_date_picker'}),
        help_text=_('When this event start')
    )

    start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'id': 'initial_hour_picker'}),
        help_text=_('At what time this event start')
    )

    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'id': 'final_date_picker'}),
        help_text=_('When this even end')
    )

    end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'id': 'final_hour_picker'}),
        help_text=_('At what time this event end')
    )

    all_day = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'switch_event_hours'}),
        help_text=_('Check if this event is for all day or not'),
    )

    event_type = forms.ChoiceField(
        choices=EventFormChoices.choices,
        required=True,
        help_text=_('Type of the event')
    )

    campaing = forms.CharField(
        max_length='256',
        required=True,
        help_text=_('Asociated campaign of this event')
    )

    installation = forms.CharField(
        max_length='256',
        required=True,
        help_text=_('Asociated installation of this event')
    )

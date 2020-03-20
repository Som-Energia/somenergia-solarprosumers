from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth.models import User

from .models import (Client, Project, Technical_campaign,
                     Technical_details)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class ClientForm(forms.ModelForm):
    class Meta():
        model = Client
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    'campaign',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'client',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'is_invalid_prereport',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'status',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'warning',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'is_cch_downloaded',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'date_prereport',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'is_invalid_prereport',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Project
        fields = [
            'date_prereport',
            'is_invalid_prereport',
            'status',
            'warning',
            'is_cch_downloaded',
            'campaign',
            'client'
        ]


class PrereportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrereportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_prereport',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'is_invalid_prereport',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))

    class Meta:
        model = Project
        fields = [
            'date_prereport',
            'is_invalid_prereport',
            'upload_prereport',
            'campaign',
            'client'
        ]

    def prereport(self, date_prereport_review, is_invalid_prereport):
        date_prereport = date_prereport_review
        if is_invalid_prereport:
            status = 'prereport review'
            warning = 'No Warn'
            return status, date_prereport, warning
        else:
            status = 'prereport'
            warning = 'No Warn'
            return status, date_prereport, warning


class TechnicalVisitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TechnicalVisitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'date_technical_visit',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))

    class Meta:
        model = Project
        fields = [
            'date_technical_visit',
            'campaign',
            'client'
        ]
        widgets = {
            'date_technical_visit': DatePickerInput(),
        }

    def set_technical_visit(self, date_set_technical_visit):
        date_technical_visit = date_set_technical_visit
        status = 'technical visit'
        warning = 'No Warn'
        return status, date_technical_visit, warning


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_report',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'is_invalid_report',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))

    class Meta:
        model = Project
        fields = [
            'date_report',
            'is_invalid_report',
            'upload_report',
            'campaign',
            'client'
        ]

    def report(self, date_upload_report, is_invalid_report):
        date_report = date_upload_report
        if self.cleaned_data['is_invalid_report']:
            status = 'report review'
            warning = 'No Warn'
            return status, date_report, warning
        else:
            status = 'report'
            warning = 'No Warn'
            return status, date_report, warning


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_offer',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'is_invalid_offer',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_offer',
            'is_invalid_offer',
            'upload_offer',
            'campaign',
            'client'
        ]

    def offer(self, date_upload_offer, is_invalid_offer):
        date_offer = date_upload_offer
        if self.cleaned_data['is_invalid_offer']:
            status = 'offer review'
            warning = 'No Warn'
            return status, date_offer, warning
        else:
            status = 'offer'
            warning = 'No Warn'
            return status, date_offer, warning


class SignedContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignedContractForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_contract',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_signature',
            'upload_contract',
            'campaign',
            'client'
        ]


class ConstructionPermitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConstructionPermitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_permit',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_permit',
            'upload_permit',
            'campaign',
            'client'
        ]

    def construction_permit(self, date_permit):
        if date_permit:
            status = 'construction permit'
            warning = 'No Warn'
            return status, warning
        else:
            status = 'signature'
            warning = 'No Warn'
            return status, warning


class DeliveryCertificateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryCertificateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_delivery_certificate',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_delivery_certificate',
            'upload_delivery_certificate',
            'campaign',
            'client'
        ]


class LegalizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegalizationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_legal_docs',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_legal_docs',
            'upload_legal_docs',
            'campaign',
            'client'
        ]

class LegalRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegalRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'upload_legal_registration_docs',
                    css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_legal_registration_docs',
            'upload_legal_registration_docs',
            'campaign',
            'client'
        ]


class InstallationDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstallationDateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('campaign', disabled=True),
                    css_class='col-sm-4 read-only'),
                Column(
                    Field('client', disabled=True),
                    css_class='col-sm-4 read-only'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'date_start_installation',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Project
        fields = [
            'date_start_installation',
            'is_date_set',
            'campaign',
            'client'
        ]
        widgets = {
            'date_start_installation': DatePickerInput(),
        }

    def set_date_installation(self, date_installation):
        if date_installation:
            status = 'date installation set'
            is_date_set = True
            warning = 'No Warn'
            return status, is_date_set, warning
        else:
            status = 'pending installation date'
            is_date_set = False
            warning = 'installation date'
            return status, is_date_set, warning


class TechnicalDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TechnicalDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['project'].disabled = True
        self.fields['campaign'].disabled = True
        self.fields['client'].disabled = True
        self.helper.layout = Layout(
            Row(
                Column(
                    'project',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'campaign',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'client',
                    css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'administrative_division',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'municipality',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'street',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'town',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'postal_code',
                    css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'contract_number',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    'cups',
                    css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column(
                    'roof_orientation',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    'solar_modules_angle',
                    css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'voltage',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'tariff',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'anual_consumption',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'installation_power',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'installation_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'installation_singlephase_model',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'installation_threephase_model',
                    css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'homemanager',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'power_meter',
                    css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'acquire_interest',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    'client_comments',
                    css_class='form-group col-md-8 mb-0'),
                Column(
                    'engineering_comments',
                    css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'bateries_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'bateries_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'bateries_power',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'bateries_capacity',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'bateries_price',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'shadow_optimizer',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'shadow_optimizer_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'shadow_optimizer_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'shadow_optimizer_price',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'count_panels',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'peak_power_panels_wp',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'panel_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'panel_type',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'panel_model',
                    css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column(
                    'inversor_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'inversor_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'nominal_inversor_power',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'electric_car_charger',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'charger_brand',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'charger_manager',
                    css_class='form-group col-md-3 mb-0'),
                Column(
                    'charger_manager_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'charger_manager_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'charger_manager_price',
                    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'electric_car',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'electric_car_charger_brand',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'electric_car_charger_model',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'electric_car_charger_power',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'electric_car_charger_price',
                    css_class='form-group col-md-4 mb-0'),
            ),

        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))
        self.helper.layout.append(Submit('cancel', 'cancel'))

    class Meta:
        model = Technical_details
        fields = '__all__'


class TechnicalCampaignsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TechnicalCampaignsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['campaign'].disabled = True
        self.helper.layout = Layout(
            Row(
                Column(
                    'campaign',
                    css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column(
                    'price_mono_fixed',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'price_mono_var',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'price_tri_fixed',
                    css_class='form-group col-md-4 mb-0'),
                Column(
                    'price_tri_var',
                    css_class='form-group col-md-4 mb-0'),
            ),
        )

        self.helper.layout.append(Submit('goback', 'Go back'))

    class Meta:
        model = Technical_campaign
        fields = '__all__'

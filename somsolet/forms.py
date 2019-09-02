from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from django_tables2 import tables, TemplateColumn

from .models import Project, Technical_details, Client, Engineering, UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_invalid_prereport', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('warning', css_class='form-group col-md-4 mb-0'),
                Column('is_data_sent', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_prereport', css_class='form-group col-md-4 mb-0'),
                Column('is_invalid_prereport', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Project
        fields = ['date_prereport', 'is_invalid_prereport', 'status', 'warning', 'is_data_sent', 'campaign', 'client']


class PrereportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrereportForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('upload_prereport', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_invalid_prereport', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('cancel', 'cancel'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))

    class Meta:
        model = Project
        fields = ['date_prereport', 'is_invalid_prereport', 'upload_prereport', 'campaign', 'client']


    def prereport(self, date_prereport_review, is_invalid_prereport):
        date_prereport = date_prereport_review
        if self.cleaned_data['is_invalid_prereport']:
            status = 'prereport review'
            return status, date_prereport
        else:
            status = 'technical visit'
            return status, date_prereport


class TechnicalVisitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TechnicalVisitForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_technical_visit', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
        self.helper.layout.append(Submit('save', 'save'))
        self.helper.layout.append(Submit('next', 'next'))

    class Meta:
        model = Project
        fields = ['date_technical_visit', 'campaign', 'client']

    def set_technical_visit(self, date_set_technical_visit):
        date_technical_visit = date_set_technical_visit
        status = 'technical visit'
        return status, date_technical_visit


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('upload_report', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_invalid_report', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(Submit('previous', 'previous'))
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
            status = 'offer'
            warning = 'No Warn'
            return status, date_report, warning


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('upload_offer', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_invalid_offer', css_class='form-group col-md-12 mb-0'),
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
            status = 'signature'
            warning = 'No Warn'
            return status, date_offer, warning


class ConstructionPermitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConstructionPermitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('upload_permit', css_class='form-group col-md-12 mb-0'),
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


class InstallationDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstallationDateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
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

    def set_date_installation(self, date_installation):
        if self.cleaned_data['date_start_installation']:
            status = 'date installation set'
            is_date_set = True
            return status, is_date_set
        else:
            status = 'date_permit'
            is_date_set = False
            return status, is_date_set



class TechnicalDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TechnicalDetailsForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('project', css_class='form-group col-md-4 mb-0'),
                Column('campaign', css_class='form-group col-md-4 mb-0'),
                Column('client', css_class='form-group col-md-4 mb-0'),
                Column('engineering', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('street', css_class='form-group col-md-7 mb-0'),
                Column('town', css_class='form-group col-md-3 mb-0'),
                Column('postal_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('contract_number', css_class='form-group col-md-6 mb-0'),
                Column('cups', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('roof_orientation', css_class='form-group col-md-6 mb-0'),
                Column('solar_modules_angle', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('voltage', css_class='form-group col-md-4 mb-0'),
                Column('peak_power_panels_wp', css_class='form-group col-md-4 mb-0'),
                Column('installation_power', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('panel_brand', css_class='form-group col-md-3 mb-0'),
                Column('panel_type', css_class='form-group col-md-3 mb-0'),
                Column('panel_model', css_class='form-group col-md-3 mb-0'),
                Column('count_panels', css_class='form-group col-md-3 mb-0'),  
                css_class='form-row'
            ),
            Row(
                Column('inversor_brand', css_class='form-group col-md-4 mb-0'),
                Column('nominal_inversor_power', css_class='form-group col-md-4 mb-0'),
                Column('inversor_model', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('bateries_brand', css_class='form-group col-md-3 mb-0'),
                Column('bateries_power', css_class='form-group col-md-3 mb-0'),
                Column('bateries_model', css_class='form-group col-md-3 mb-0'),
                Column('bateries_capacity', css_class='form-group col-md-3 mb-0'), 
                css_class='form-row'
            ),
            Row(
                Column('homemanager', css_class='form-group col-md-6 mb-0'),
                Column('electric_car', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),

        )
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Technical_details
        fields = '__all__'

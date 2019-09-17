import csv
import logging
from datetime import datetime

import pymongo
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django_tables2 import RequestConfig

from .filters import CampaignListFilter, ProjectListFilter
from .forms import (ClientForm, ConstructionPermitForm, InstallationDateForm,
                    OfferForm, PrereportForm, ReportForm,
                    TechnicalCampaignsForm, TechnicalDetailsForm,
                    TechnicalVisitForm, UserForm)
from .models import (Campaign, Client, Engineering, Project,
                     Technical_campaign, Technical_details)
from .tables import CampaignTable, ProjectTable

logger = logging.getLogger(__name__)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect(reverse('project'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(
        request,
        'registration/registration.html',
        {
            'user_form': user_form,
            'registered': registered
        }
    )


class SomsoletProjectView(View):

    def get_initial(self, pk):
        proj_inst = get_object_or_404(Project, pk=pk)
        return {
            'campaign': proj_inst.campaign,
            'project': proj_inst.id,
            'client': proj_inst.client,
        }

    def get(self, request, pk):
        self.initial = self.get_initial(pk)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {self.form: form})

    def button_options(self, request, pk, proj_inst):
        if 'next' in request.POST:
            proj_inst.save()
            next_proj = Project.objects.filter(
                campaign=proj_inst.campaign,
                pk__gt=pk
            ).order_by('pk').first() or Project.objects.filter(
                campaign=proj_inst.campaign
            ).first()
            return HttpResponseRedirect(reverse(
                self.url_path,
                args=[next_proj.id])
            )
        elif 'previous' in request.POST:
            proj_inst.save()
            previous_proj = Project.objects.filter(
                campaign=proj_inst.campaign,
                pk__lt=pk
            ).order_by('pk').last() or Project.objects.filter(
                campaign=proj_inst.campaign
            ).last()
            return HttpResponseRedirect(reverse(
                self.url_path,
                args=[previous_proj.id]))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse(
                'project',
                args=[proj_inst.campaign.pk]))
        elif 'save' in request.POST:
            proj_inst.save()
            return HttpResponseRedirect(reverse(
                'project',
                args=[proj_inst.campaign.pk]))


class PrereportView(SomsoletProjectView):
    form_class = PrereportForm
    template_name = 'somsolet/prereport.html'
    model = Project

    def __init__(self):
        self.form = 'prereportform'
        self.url_path = 'prereport'

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_prereport = datetime.now().strftime('%Y-%m-%d')
            prereport_invalid = form.cleaned_data['is_invalid_prereport']
            status, date_prereport, warn = form.prereport(
                date_prereport_review=date_prereport,
                is_invalid_prereport=prereport_invalid,)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.upload_prereport = form.cleaned_data['upload_prereport']
            proj_inst.is_invalid_prereport = prereport_invalid
            if request.FILES:
                proj_inst.date_prereport = date_prereport
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'prereportform': form})


class TechnicalVisitView(SomsoletProjectView):
    form_class = TechnicalVisitForm
    template_name = 'somsolet/technical_visit.html'

    def __init__(self):
        self.form = 'technicalvisitform'
        self.url_path = 'technical_visit'

    def post(self, request, pk):
        form = self.form_class(request.POST)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_technical_visit = form.cleaned_data['date_technical_visit']
            status, date_technical_visit, warn = form.set_technical_visit(
                date_set_technical_visit=date_technical_visit)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.date_technical_visit = date_technical_visit
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'technicalvisitform': form})


class ReportView(SomsoletProjectView):
    form_class = ReportForm
    template_name = 'somsolet/report.html'

    def __init__(self):
        self.form = 'reportform'
        self.url_path = 'report'

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_report = datetime.now().strftime('%Y-%m-%d')
            report_invalid = form.cleaned_data['is_invalid_report']
            status, date_report, warn = form.report(
                date_upload_report=date_report,
                is_invalid_report=report_invalid)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.upload_report = form.cleaned_data['upload_report']
            proj_inst.is_invalid_report = report_invalid
            if request.FILES:
                proj_inst.date_report = date_report
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'reportform': form})


class OfferView(SomsoletProjectView):
    form_class = OfferForm
    template_name = 'somsolet/offer.html'

    def __init__(self):
        self.form = 'offerform'
        self.url_path = 'offer'

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_offer = datetime.now().strftime('%Y-%m-%d')
            offer_invalid = form.cleaned_data['is_invalid_offer']
            status, date_offer, warn = form.offer(
                date_upload_offer=date_offer,
                is_invalid_offer=offer_invalid)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.upload_offer = form.cleaned_data['upload_offer']
            proj_inst.is_invalid_offer = offer_invalid
            if request.FILES:
                proj_inst.date_offer = date_offer
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'offerform': form})


class ConstructionPermitView(SomsoletProjectView):
    form_class = ConstructionPermitForm
    template_name = 'somsolet/construction_permit.html'

    def __init__(self):
        self.form = 'constructionpermitform'
        self.url_path = 'construction_permit'

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_permit = datetime.now().strftime('%Y-%m-%d')
            status, warn = form.construction_permit(
                date_permit=date_permit)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.upload_permit = form.cleaned_data['upload_permit']
            if request.FILES:
                proj_inst.date_permit = date_permit
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'constructionpermitform': form})


class InstallationDateView(SomsoletProjectView):
    form_class = InstallationDateForm
    template_name = 'somsolet/installation_date.html'

    def __init__(self):
        self.form = 'installationdateform'
        self.url_path = 'installation_date'

    def post(self, request, pk):
        form = self.form_class(request.POST)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            date_installation = form.cleaned_data['date_start_installation']
            status, is_date_set, warn = form.set_date_installation(
                date_installation=date_installation)
            proj_inst.status = status
            proj_inst.warning = warn
            proj_inst.is_date_set = is_date_set
            proj_inst.date_start_installation = date_installation
            return self.button_options(request, pk, proj_inst)

        return render(request, self.template_name, {'installationdateform': form})


class ClientView(DetailView):
    model = Client


class CampaignSetView(View):
    template_name = 'somsolet/campaign.html'

    def get(self, request):
        campaign_filter = CampaignListFilter(
            request,
            queryset=Campaign.objects.all().filter(
                engineering=request.user.engineering))
        campaign_list = campaign_filter.qs
        campaign_table = CampaignTable(campaign_list)
        ctx = {
            'campaign': campaign_table,
        }
        return render(request, self.template_name, ctx)


class ProjectView(View):
    template_name = 'somsolet/project_detail.html'

    def get(self, request, pk):
        campaign_inst = get_object_or_404(Campaign, pk=pk)
        project_filter = ProjectListFilter(
            request.GET,
            queryset=Project.objects.all().filter(campaign=campaign_inst.id))
        project_list = project_filter.qs
        projects_table = ProjectTable(project_list)

        ctx = {
            'project': projects_table,
            'filter': project_filter
        }
        RequestConfig(
            request,
            paginate={'per_page': 20}
        ).configure(projects_table)
        return render(request, 'somsolet/project_detail.html', ctx)


class DownloadCch(View):
    url_path = 'download_cch'

    def get(self, request, pk): # Autentication required
        project = Project.objects.get(pk=pk)
        technical_details = project.technical_details_set.first()
        cups = technical_details.cups

        client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
            settings.DATABASES['mongodb']['USER'],
            settings.DATABASES['mongodb']['PASSWORD'],
            settings.DATABASES['mongodb']['HOST'],
            settings.DATABASES['mongodb']['PORT'],
            settings.DATABASES['mongodb']['NAME'],
            )
        )
        db = client[settings.DATABASES['mongodb']['NAME']]

        cursor = db.tg_cchfact.find({
            "name": {'$regex': '^{}'.format(cups[:20])}
        })

        if cursor.count() == 0:
            return HttpResponseRedirect(reverse(
                'project',
                args=[project.campaign.pk])
            )
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="cch_project_{}.csv"'.format(cups)
            writer = csv.writer(response)

            writer.writerow(['Project', 'date', 'value', 'units'])
            for measure in cursor:
                writer.writerow([
                    project.name,
                    measure['datetime'],
                    measure['ai'],
                    'Wh'
                ])
            cursor.close()
            client.close()
            return response


class TechnicalCampaignsView(View):
    form_class = TechnicalCampaignsForm
    template_name = 'somsolet/technical_details.html'
    url_path = 'technical_campaign'

    def get_initial_values(self, pk):
        campaign_inst = get_object_or_404(Campaign, pk=pk)
        tech_details = Technical_campaign.objects.get(campaign=campaign_inst.id)
        return tech_details

    def get(self, request, pk):
        self.initial = self.get_initial_values(pk)
        form = self.form_class(instance=self.initial)
        return render(
            request,
            self.template_name, {'technical_form': form}
        )

    def post(self, request, pk):
        self.initial = self.get_initial_values(pk)
        form = self.form_class(self.request.POST, instance=self.initial)
        campaign_inst = get_object_or_404(Campaign, pk=pk)
        if form.is_valid():
            return HttpResponseRedirect(reverse('campaign'))
        return render(
            request,
            self.template_name, {'technical_form': form}
        )


class TechnicalDetailsView(View):
    form_class = TechnicalDetailsForm
    template_name = 'somsolet/technical_details.html'
    url_path = 'technical_details'

    def get_initial_values(self, pk):
        proj_inst = get_object_or_404(Project, pk=pk)
        tech_details = Technical_details.objects.get(project=proj_inst.id)
        return tech_details

    def get(self, request, pk):
        self.initial = self.get_initial_values(pk)
        form = self.form_class(instance=self.initial)
        return render(
            request,
            self.template_name, {'technical_form': form}
        )

    def post(self, request, pk):
        self.initial = self.get_initial_values(pk)
        form = self.form_class(self.request.POST, instance=self.initial)
        proj_inst = get_object_or_404(Project, pk=pk)
        if form.is_valid():
            form.campaign = proj_inst.campaign
            form.save()
            return self.button_options(request, pk, proj_inst)
        return render(
            request,
            self.template_name, {'technical_form': form}
        )

    def button_options(self, request, pk, proj_inst):
        if 'next' in request.POST:
            proj_inst.save()
            next_proj = Project.objects.filter(
                campaign=proj_inst.campaign,
                pk__gt=pk
            ).order_by('pk').first() or Project.objects.filter(
                campaign=proj_inst.campaign
            ).first()
            return HttpResponseRedirect(reverse(
                self.url_path,
                args=[next_proj.id])
            )
        elif 'previous' in request.POST:
            proj_inst.save()
            previous_proj = Project.objects.filter(
                campaign=proj_inst.campaign,
                pk__lt=pk
            ).order_by('pk').last() or Project.objects.filter(
                campaign=proj_inst.campaign
            ).last()
            return HttpResponseRedirect(reverse(
                self.url_path,
                args=[previous_proj.id]))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse(
                'project',
                args=[proj_inst.campaign.pk]))
        elif 'save' in request.POST:
            proj_inst.save()
            return HttpResponseRedirect(reverse(
                'project',
                args=[proj_inst.campaign.pk]))

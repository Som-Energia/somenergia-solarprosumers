from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django_tables2 import RequestConfig, SingleTableView
from datetime import datetime

from .models import Technical_details, Project, Campaign, Engineering, Client, UserProfileInfo
from .forms import TechnicalDetailsForm, PrereportForm, ProjectForm, UserForm, ReportForm
from .forms import TechnicalVisitForm, OfferForm, ConstructionPermitForm, InstallationDateForm
from .tables import ProjectTable
from .filters import ProjectListFilter


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


def campaign(request, pk):
    num_projects = Project.objects.all().count()
    num_clients = Client.objects.all().count()
    campaign_details = Project.objects.all()
    return render(
        request,
        'somsolet/campaign_details.html',
        {
            'campaign': campaign_details,
            'num_proj': num_projects,
            'num_clients': num_clients
        }
    )


def prereport(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = PrereportForm(request.POST, request.FILES)
        print(form.errors)

        if form.is_valid():
            date_prereport = datetime.now().strftime('%Y-%m-%d')
            prereport_invalid = form.cleaned_data['is_invalid_prereport']
            status, date_prereport = form.prereport(
                date_prereport_review=date_prereport,
                is_invalid_prereport=prereport_invalid)
            proj_inst.status = status
            proj_inst.upload_prereport = form.cleaned_data['upload_prereport']
            if request.FILES:
                proj_inst.date_prereport = date_prereport
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'prereport',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'prereport',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = PrereportForm()
    return render(request, 'somsolet/prereport.html', {'prereportform': form})


def technical_visit(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = TechnicalVisitForm(request.POST)
        print(form.errors)
        if form.is_valid():
            date_technical_visit = datetime.now().strftime('%Y-%m-%d')
            status, date_technical_visit = form.set_technical_visit(
                date_set_technical_visit=date_technical_visit)
            proj_inst.status = status
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'technical_visit',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'technical_visit',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = TechnicalVisitForm()
    return render(request, 'somsolet/technical_vist.html', {'technicalvisitform': form})

def report(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            date_report = datetime.now().strftime('%Y-%m-%d')
            report_invalid = form.cleaned_data['is_invalid_report']
            status, date_report = form.report(
                date_upload_report=date_report,
                is_invalid_report=report_invalid)
            proj_inst.status = status
            proj_inst.upload_report = form.cleaned_data['upload_report']
            if request.FILES:
                proj_inst.date_report = date_report
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'report',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'report',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = ReportForm()
    return render(request, 'somsolet/report.html', {'reportform': form})


def offer(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            date_offer = datetime.now().strftime('%Y-%m-%d')
            offer_invalid = form.cleaned_data['is_invalid_offer']
            status, date_offer = form.offer(
                date_upload_offer=date_offer,
                is_invalid_offer=offer_invalid)
            proj_inst.status = status
            proj_inst.upload_offer = form.cleaned_data['upload_offer']
            if request.FILES:
                proj_inst.date_offer = date_offer
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'offer',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'offer',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = OfferForm()
    return render(request, 'somsolet/offer.html', {'offerform': form})


def construction_permit(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ConstructionPermitForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            date_permit = datetime.now().strftime('%Y-%m-%d')
            status, date_permit = form.construction_permit(
                date_permit=date_permit)
            proj_inst.status = status
            proj_inst.upload_permit = form.cleaned_data['upload_permit']
            if request.FILES:
                proj_inst.date_permit = date_permit
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'construction_permit',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'construction_permit',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = ConstructionPermitForm()
    return render(request, 'somsolet/construction_permit.html', {'constructionpermitform': form})


def set_date_installation(request, pk):
    proj_inst = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = InstallationDateForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            date_installation = form.cleaned_data['date_installation']
            status, is_date_set, date_start_installation = form.set_date_installation(
                date_installation=date_installation)
            proj_inst.status = status
            proj_inst.is_date_set = is_date_set
            proj_inst.date_start_installation = date_installation
            if 'next' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'installation_date',
                    args=[proj_inst.id + 1]))
            elif 'previous' in request.POST:
                proj_inst.save()
                return HttpResponseRedirect(reverse(
                    'installation_date',
                    args=[proj_inst.id - 1]))
            elif 'cancel' in request.POST:
                return redirect('project')
            proj_inst.save()
            return redirect('project')

    else:
        form = InstallationDateForm()
    return render(request, 'somsolet/installation_date.html', {'installationdateform': form})


class ClientView(DetailView):
    model = Client

def project(request):
    project_filter = ProjectListFilter(request.GET, queryset=Project.objects.all())

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

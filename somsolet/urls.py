from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path(
        'profile_engineering/',
        views.CampaignSetView.as_view(),
        name='campaign',
    ),
    path(
        'client/<int:pk>/',
        views.ClientView.as_view(template_name='somsolet/client_detail.html'),
        name='client',
    ),
    path(
        'download_cch/<int:pk>/',
        views.DownloadCch.as_view(),
        name='download_cch'
    ),
    path(
        'technical_details/<int:pk>/',
        views.TechnicalDetailsView.as_view(),
        name='technical_details'
    ),
    path(
        'technical_campaign/<int:pk>/',
        views.TechnicalCampaignsView.as_view(),
        name='technical_campaign'
    ),
    path(
        'project/<int:pk>/',
        views.ProjectView.as_view(),
        name='project'),
    path(
        'prereport/<int:pk>/',
        views.PrereportView.as_view(),
        name='prereport'
    ),
    path(
        'technical_visit/<int:pk>/',
        views.TechnicalVisitView.as_view(),
        name='technical_visit'
    ),
    path(
        'report/<int:pk>/',
        views.ReportView.as_view(),
        name='report'
    ),
    path(
        'offer/<int:pk>/',
        views.OfferView.as_view(),
        name='offer'
    ),
    path(
        'construction_permit/<int:pk>/',
        views.ConstructionPermitView.as_view(),
        name='construction_permit'
    ),
    path(
        'installation_date/<int:pk>/',
        views.InstallationDateView.as_view(),
        name='installation_date'
    ),
    path(
        'delivery_certificate/<int:pk>/',
        views.DeliveryCertificateView.as_view(),
        name='delivery_certificate'
    ),
    path(
        'legalization/<int:pk>/',
        views.LegalizationView.as_view(),
        name='legalization'
    ),
    path('register/', views.register, name='register'),

]

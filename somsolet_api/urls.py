from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (CampaignViewSet, CchDownloadViewSet,
                    DeliveryCertificateViewSet, FirstInvoiceViewSet,
                    LastInvoiceViewSet, LegalizationViewSet,
                    LegalRegistrationViewSet, OfferViewSet, OfferAcceptedViewSet, PermitViewSet,
                    PrereportViewSet, ProjectViewSet, RenkontoEventView,
                    ReportViewSet, SecondInvoiceViewSet, SignatureViewSet,
                    StagesListViewSet, StatsViewSet, TechnicalDetailsViewSet)

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet, basename='campaign')
router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'stages', StagesListViewSet, basename='stages_list')
router.register(r'cch', CchDownloadViewSet, basename='cch')
router.register(r'prereport', PrereportViewSet, basename='prereport')
router.register(r'report', ReportViewSet, basename='report')
router.register(r'first_invoice', FirstInvoiceViewSet, basename='first_invoice')
router.register(r'second_invoice', SecondInvoiceViewSet, basename='second_invoice')
router.register(r'last_invoice', LastInvoiceViewSet, basename='last_invoice')
router.register(r'signature', SignatureViewSet, basename='signature')
router.register(r'permit', PermitViewSet, basename='permit')
router.register(r'offer', OfferViewSet, basename='offer')
router.register(r'offer_accepted', OfferAcceptedViewSet, basename='offer_accepted')
router.register(r'legal_registration', LegalRegistrationViewSet, basename='legal_registration')
router.register(r'legalization', LegalizationViewSet, basename='legalization')
router.register(r'technical_details', TechnicalDetailsViewSet, basename='technical_details')
router.register(r'delivery_certificate', DeliveryCertificateViewSet, basename='delivery_certificate')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(
        'events/<int:engineering_id>',
        RenkontoEventView.as_view(),
        name='events'
    ),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns += router.urls

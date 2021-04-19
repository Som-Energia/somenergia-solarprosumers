from django.urls import include, path
from rest_framework import routers

from .views import (CampaignViewSet, CchDownloadViewSet, ProjectViewSet, PrereportViewSet,
                    RenkontoEventViewSet, ReportViewSet, StagesViewSet)

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet, basename='campaign')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'stages', StagesViewSet, basename='stages')
router.register(r'event', RenkontoEventViewSet)
router.register(r'cch', CchDownloadViewSet, basename='cch')
router.register(r'prereport', PrereportViewSet, basename='prereport')
router.register(r'report', ReportViewSet, basename='report')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

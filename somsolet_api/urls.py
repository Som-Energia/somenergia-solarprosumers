from django.urls import include, path
from rest_framework import routers

from .views import (CampaignViewSet, ProjectViewSet, RenkontoEventView,
    StagesViewSet)

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet)
router.register(r'project', ProjectViewSet)
router.register(r'stages', StagesViewSet, basename='stages')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(
        'events/<int:engineering_id>',
        RenkontoEventView.as_view(),
        name='events'
    ),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls

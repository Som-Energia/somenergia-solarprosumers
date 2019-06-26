from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('campaign/<int:pk>/', views.campaign, name='campaign'),
    path('technical_details/<int:pk>/', views.technical_details, name='technical_details'),
    path('project/', views.project, name='project'),
    path('prereport/<int:pk>/', views.prereport, name='prereport'),
    path('technical_visit/<int:pk>/', views.technical_visit, name='technical_visit'),
    path('report/<int:pk>/', views.report, name='report'),
    path('offer/<int:pk>/', views.offer, name='offer'),
    path('construction_permit/<int:pk>/', views.construction_permit, name='construction_permit'),
    path('installation_date/<int:pk>/', views.set_date_installation, name='installation_date'),

    path('register/',views.register, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""somsolet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from somsolet import views

app_name = "config"

urlpatterns = [
    path("", views.CampaignSetView.as_view()),
    path("auth/", include("django.contrib.auth.urls")),
    path("somsolet/", include("somsolet.urls")),
    path("admin/", admin.site.urls),
    path("django-rq/", include("django_rq.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("hijack/", include("hijack.urls")),
]

if settings.DEBUG:
    urlpatterns += (
        [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

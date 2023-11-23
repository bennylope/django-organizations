from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from organizations.backends import invitation_backend
from organizations.backends import registration_backend

urlpatterns = [
    path("admin/", admin.site.urls),
    path("organizations/", include("organizations.urls")),
    path("invite/", include(invitation_backend().get_urls())),
    path("register/", include(registration_backend().get_urls())),
]

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path

from organizations.backends import invitation_backend
from organizations.backends import registration_backend

admin.autodiscover()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("organizations/", include("organizations.urls")),
    path("invite/", include(invitation_backend().get_urls())),
    path("register/", include(registration_backend().get_urls())),
    path("accounts/", include("test_accounts.urls", namespace="test_accounts")),
] + staticfiles_urlpatterns("/static/")

from django.conf.urls import url
from django.contrib import admin

from organizations.backends import registration_backend

admin.autodiscover()

app_name = "test_accounts"

urlpatterns = [
    url(
        r"^register/",
        registration_backend(
            backend="test_accounts.backends.AccountRegistration", namespace="test_accounts"
        ).urls
    )
]

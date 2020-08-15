from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from organizations.backends.modeled import ModelInvitation
from test_accounts.models import Account

admin.autodiscover()

app_name = "test_accounts"

urlpatterns = [
    path(
        "register/",
        include(
            ModelInvitation(org_model=Account, namespace="invitations").urls,
            namespace="account_invitations",
        ),
    )
]

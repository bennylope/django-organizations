from django.db import models
from django.urls import reverse

from organizations.base import OrganizationBase
from organizations.base import OrganizationInvitationBase
from organizations.base import OrganizationOwnerBase
from organizations.base import OrganizationUserBase


class Account(OrganizationBase):
    monthly_subscription = models.IntegerField(default=1000)


class AccountUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default="")


class AccountOwner(OrganizationOwnerBase):
    pass


class AccountInvitation(OrganizationInvitationBase):

    def get_absolute_url(self):
        """Returns the invitation URL"""
        return reverse(
            "test_accounts:account_invitations:invitations_register",
            kwargs={"guid": str(self.guid).replace("-", "")},
        )

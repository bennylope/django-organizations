from django.db import models
from organizations.base import OrganizationBase
from organizations.base import OrganizationUserBase
from organizations.base import OrganizationOwnerBase
from organizations.base import OrganizationInvitationBase
from django.shortcuts import reverse


class Account(OrganizationBase):
    monthly_subscription = models.IntegerField(default=1000)


class AccountUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default="")


class AccountOwner(OrganizationOwnerBase):
    pass


class AccountInvitation(OrganizationInvitationBase):
    def get_absolute_url(self):
        """Returns the invitation URL"""
        return reverse("test_accounts:account_invitations:registration_create", kwargs={'guid': self.guid})

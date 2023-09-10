from django.db import models

from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationInvitation,
    AbstractOrganizationOwner,
    AbstractOrganizationUser,
)


class Account(AbstractOrganization):
    monthly_subscription = models.IntegerField(default=1000)


class AccountUser(AbstractOrganizationUser):
    user_type = models.CharField(max_length=1, default="")


class AccountOwner(AbstractOrganizationOwner):
    pass


class AccountInvitation(AbstractOrganizationInvitation):
    pass

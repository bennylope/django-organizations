from django.db import models
from organizations.base import (OrganizationBase, OrganizationUserBase,
                                OrganizationOwnerBase)


class Account(OrganizationBase):
    monthly_subscription = models.IntegerField(default=1000)


class AccountUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default='')


class AccountOwner(OrganizationOwnerBase):
    pass

from django.db import models
from organizations.base import (OrganizationBase, OrganizationUserBase,
                                OrganizationOwnerBase)


class Vendor(OrganizationBase):
    monthly_subscription = models.IntegerField(default=1000)


class VendorUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default='')


class VendorOwner(OrganizationOwnerBase):
    pass

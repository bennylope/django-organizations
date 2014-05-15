from django.contrib.auth.models import Permission
from django.db import models
from organizations.base import (OrganizationBase, OrganizationUserBase,
                                OrganizationOwnerBase)


class Vendor(OrganizationBase):
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')


class VendorUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default='')
    permissions = models.ManyToManyField(Permission, blank=True)


class VendorOwner(OrganizationOwnerBase):
    pass

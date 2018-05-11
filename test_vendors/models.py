from django.contrib.auth.models import Permission
from django.db import models
from organizations.base import OrganizationBase
from organizations.base import OrganizationUserBase
from organizations.base import OrganizationOwnerBase
from organizations.base import OrganizationInvitationBase


class Vendor(OrganizationBase):
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')


class VendorUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default='')
    permissions = models.ManyToManyField(Permission, blank=True)


class VendorOwner(OrganizationOwnerBase):
    pass


class VendorInvitation(OrganizationInvitationBase):
    pass

from django.contrib.auth.models import Permission
from django.db import models

from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationInvitation,
    AbstractOrganizationOwner,
    AbstractOrganizationUser,
)


class Vendor(AbstractOrganization):
    street_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="vendors"
    )


class VendorUser(AbstractOrganizationUser):
    user_type = models.CharField(max_length=1, default="")
    permissions = models.ManyToManyField(Permission, blank=True)


class VendorOwner(AbstractOrganizationOwner):
    pass


class VendorInvitation(AbstractOrganizationInvitation):
    pass

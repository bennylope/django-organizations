from django.contrib.auth.models import Permission
from django.db import models

from organizations.abstract import AbstractOrganization
from organizations.abstract import AbstractOrganizationInvitation
from organizations.abstract import AbstractOrganizationOwner
from organizations.abstract import AbstractOrganizationUser


class CustomOrganization(AbstractOrganization):
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')


class CustomUser(AbstractOrganizationUser):
    user_type = models.CharField(max_length=1, default='')
    permissions = models.ManyToManyField(Permission, blank=True)


class CustomOwner(AbstractOrganizationOwner):
    pass


class CustomInvitation(AbstractOrganizationInvitation):
    pass

from django.contrib.auth.models import Permission
from django.db import models
from organizations.abstract import (AbstractOrganization,
                                    AbstractOrganizationUser,
                                    AbstractOrganizationOwner)


class CustomOrganization(AbstractOrganization):
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')


class CustomUser(AbstractOrganizationUser):
    user_type = models.CharField(max_length=1, default='')
    permissions = models.ManyToManyField(Permission, blank=True)


class CustomOwner(AbstractOrganizationOwner):
    pass

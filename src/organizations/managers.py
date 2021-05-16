# -*- coding: utf-8 -*-

from django.db import models


class OrgManager(models.Manager):
    def get_for_user(self, user):
        return self.get_queryset().filter(users=user)


class ActiveOrgManager(OrgManager):
    """
    A more useful extension of the default manager which returns querysets
    including only active organizations
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

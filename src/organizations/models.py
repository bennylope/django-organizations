# -*- coding: utf-8 -*-

from organizations.abstract import AbstractOrganization
from organizations.abstract import AbstractOrganizationInvitation
from organizations.abstract import AbstractOrganizationOwner
from organizations.abstract import AbstractOrganizationUser


class Organization(AbstractOrganization):
    """
    Default Organization model.
    """

    class Meta(AbstractOrganization.Meta):
        abstract = False


class OrganizationUser(AbstractOrganizationUser):
    """
    Default OrganizationUser model.
    """

    class Meta(AbstractOrganizationUser.Meta):
        abstract = False


class OrganizationOwner(AbstractOrganizationOwner):
    """
    Default OrganizationOwner model.
    """

    class Meta(AbstractOrganizationOwner.Meta):
        abstract = False


class OrganizationInvitation(AbstractOrganizationInvitation):
    class Meta(AbstractOrganizationInvitation.Meta):
        abstract = False

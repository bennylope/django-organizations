# -*- coding: utf-8 -*-

class OwnershipRequired(Exception):
    """
    Exception to raise if the owner is being removed before the
    organization.
    """

    pass


class OrganizationMismatch(Exception):
    """
    Exception to raise if an organization user from a different
    organization is assigned to be an organization's owner.
    """

    pass

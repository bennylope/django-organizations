# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from organizations.models import Organization
from organizations.models import OrganizationUser


class OrganizationMixin:
    """Mixin used like a SingleObjectMixin to fetch an organization"""

    org_model = Organization
    org_context_name = "organization"

    def get_org_model(self):
        return self.org_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.org_context_name: self.organization})
        return super().get_context_data(**kwargs)

    @cached_property
    def organization(self):
        organization_pk = self.kwargs.get("organization_pk", None)
        return get_object_or_404(self.get_org_model(), pk=organization_pk)

    def get_object(self):
        return self.organization

    get_organization = get_object  # Now available when `get_object` is overridden


class OrganizationUserMixin(OrganizationMixin):
    """Mixin used like a SingleObjectMixin to fetch an organization user"""

    user_model = OrganizationUser
    org_user_context_name = "organization_user"

    def get_user_model(self):
        return self.user_model

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            {
                self.org_user_context_name: self.object,
                self.org_context_name: self.object.organization,
            }
        )
        return kwargs

    @cached_property
    def organization_user(self):
        """
        Returns the OrganizationUser object

        This is fetched based on the primary keys for both
        the organization and the organization user.
        """
        organization_pk = self.kwargs.get("organization_pk", None)
        user_pk = self.kwargs.get("user_pk", None)
        return get_object_or_404(
            self.get_user_model().objects.select_related(),
            user__pk=user_pk,
            organization__pk=organization_pk,
        )

    def get_object(self):
        """Proxy for the base class interface

        This can be called all day long and the object is queried once.
        """
        return self.organization_user


class MembershipRequiredMixin:
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if (
            not self.organization.is_member(request.user)
            and not request.user.is_superuser
        ):
            raise PermissionDenied(_("Wrong organization"))
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if (
            not self.organization.is_admin(request.user)
            and not request.user.is_superuser
        ):
            raise PermissionDenied(_("Sorry, admins only"))
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin:
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if (
            self.organization.owner.organization_user.user != request.user
            and not request.user.is_superuser
        ):
            raise PermissionDenied(_("You are not the organization owner"))
        return super().dispatch(request, *args, **kwargs)

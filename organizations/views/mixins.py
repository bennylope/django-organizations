# -*- coding: utf-8 -*-

# Copyright (c) 2012-2019, Ben Lopatin and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from organizations.models import Organization
from organizations.models import OrganizationUser


class OrganizationMixin(object):
    """Mixin used like a SingleObjectMixin to fetch an organization"""

    org_model = Organization
    org_context_name = "organization"

    def get_org_model(self):
        return self.org_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.org_context_name: self.organization})
        return super(OrganizationMixin, self).get_context_data(**kwargs)

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
        kwargs = super(OrganizationUserMixin, self).get_context_data(**kwargs)
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


class MembershipRequiredMixin(object):
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
        return super(MembershipRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminRequiredMixin(object):
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
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(object):
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
        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)

# -*- coding: utf-8 -*-

# Copyright (c) 2012-2015, Ben Lopatin and contributors
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

import warnings

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

try:
    import six
except ImportError:
    from django.utils import six

from organizations.base import OrgMeta
from organizations.base import AbstractBaseOrganization
from organizations.base import AbstractBaseOrganizationUser
from organizations.base import AbstractBaseOrganizationOwner
from organizations.fields import SlugField
from organizations.fields import AutoCreatedField
from organizations.fields import AutoLastModifiedField
from organizations.signals import user_added
from organizations.signals import user_removed
from organizations.signals import owner_changed

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
ORGS_TIMESTAMPED_MODEL = getattr(settings, 'ORGS_TIMESTAMPED_MODEL', None)

if ORGS_TIMESTAMPED_MODEL:
    warnings.warn("Configured TimestampModel has been replaced and is now ignored.",
                  DeprecationWarning)


class SharedBaseModel(models.Model):
    """
    Adds fields ``created`` and ``modified`` and
    two private methods that are used by the rest
    of the abstract models.
    """
    created = AutoCreatedField()
    modified = AutoLastModifiedField()

    @property
    def _org_user_model(self):
        model = self.__class__.module_registry[self.__class__.__module__]['OrgUserModel']
        if model is None:
            model = self.__class__.module_registry['organizations.models']['OrgUserModel']
        return model

    @property
    def _org_owner_model(self):
        model = self.__class__.module_registry[self.__class__.__module__]['OrgOwnerModel']
        if model is None:
            model = self.__class__.module_registry['organizations.models']['OrgOwnerModel']
        return model

    class Meta:
        abstract = True


class AbstractOrganization(six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganization)):
    """
    Abstract Organization model.
    """
    slug = SlugField(max_length=200, blank=False, editable=True,
            populate_from='name', unique=True,
            help_text=_("The name in all lowercase, suitable for URL identification"))

    class Meta(AbstractBaseOrganization.Meta):
        abstract = True
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization_detail', kwargs={'organization_pk': self.pk})

    def add_user(self, user, is_admin=False):
        """
        Adds a new user and if the first user makes the user an admin and
        the owner.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True
        # TODO get specific org user?
        org_user = self._org_user_model.objects.create(user=user,
                                                       organization=self,
                                                       is_admin=is_admin)
        if users_count == 0:
            # TODO get specific org user?
            self._org_owner_model.objects.create(organization=self,
                                                 organization_user=org_user)

        # User added signal
        user_added.send(sender=self, user=user)
        return org_user

    def remove_user(self, user):
        """
        Deletes a user from an organization.
        """
        org_user = self._org_user_model.objects.get(user=user,
                                                    organization=self)
        org_user.delete()

        # User removed signal
        user_removed.send(sender=self, user=user)

    def get_or_add_user(self, user, **kwargs):
        """
        Adds a new user to the organization, and if it's the first user makes
        the user an admin and the owner. Uses the `get_or_create` method to
        create or return the existing user.

        `user` should be a user instance, e.g. `auth.User`.

        Returns the same tuple as the `get_or_create` method, the
        `OrganizationUser` and a boolean value indicating whether the
        OrganizationUser was created or not.
        """
        is_admin = kwargs.pop('is_admin', False)
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True

        org_user, created = self._org_user_model.objects\
                                .get_or_create(organization=self,
                                               user=user,
                                               defaults={'is_admin': is_admin})
        if users_count == 0:
            self._org_owner_model.objects\
                .create(organization=self, organization_user=org_user)
        if created:
            # User added signal
            user_added.send(sender=self, user=user)
        return org_user, created

    def change_owner(self, new_owner):
        """
        Changes ownership of an organization.
        """
        old_owner = self.owner.organization_user
        self.owner.organization_user = new_owner
        self.owner.save()

        # Owner changed signal
        owner_changed.send(sender=self, old=old_owner, new=new_owner)

    def is_admin(self, user):
        """
        Returns True is user is an admin in the organization, otherwise false
        """
        return True if self.organization_users.filter(user=user, is_admin=True) else False

    def is_owner(self, user):
        """
        Returns True is user is the organization's owner, otherwise false
        """
        return self.owner.organization_user.user == user


class AbstractOrganizationUser(six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganizationUser)):
    """
    Abstract OrganizationUser model
    """
    is_admin = models.BooleanField(default=False)

    class Meta(AbstractBaseOrganizationUser.Meta):
        abstract = True
        verbose_name = _("organization user")
        verbose_name_plural = _("organization users")

    def __unicode__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active else
                self.user.email, self.organization.name)

    def delete(self, using=None):
        """
        If the organization user is also the owner, this should not be deleted
        unless it's part of a cascade from the Organization.

        If there is no owner then the deletion should proceed.
        """
        from organizations.exceptions import OwnershipRequired
        try:
            if self.organization.owner.organization_user.id == self.id:
                raise OwnershipRequired(_("Cannot delete organization owner "
                    "before organization or transferring ownership."))
        # TODO This line presumes that OrgOwner model can't be modified
        except self._org_owner_model.DoesNotExist:
            pass
        super(AbstractBaseOrganizationUser, self).delete(using=using)

    def get_absolute_url(self):
        return reverse('organization_user_detail', kwargs={
            'organization_pk': self.organization.pk, 'user_pk': self.user.pk})


class AbstractOrganizationOwner(six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganizationOwner)):
    """
    Abstract OrganizationOwner model
    """
    class Meta:
        abstract = True
        verbose_name = _("organization owner")
        verbose_name_plural = _("organization owners")

    def save(self, *args, **kwargs):
        """
        Extends the default save method by verifying that the chosen
        organization user is associated with the organization.

        Method validates against the primary key of the organization because
        when validating an inherited model it may be checking an instance of
        `Organization` against an instance of `CustomOrganization`. Mutli-table
        inheritence means the database keys will be identical though.

        """
        from organizations.exceptions import OrganizationMismatch
        if self.organization_user.organization.pk != self.organization.pk:
            raise OrganizationMismatch
        else:
            super(AbstractBaseOrganizationOwner, self).save(*args, **kwargs)

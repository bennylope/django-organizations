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

from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist

try:
    import six
except ImportError:
    from django.utils import six
from django.utils.translation import ugettext_lazy as _

from organizations.managers import ActiveOrgManager
from organizations.managers import OrgManager

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UnicodeMixin(object):
    """
    Python 2 and 3 string representation support.
    """
    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')


class OrgMeta(ModelBase):
    """
    Base metaclass for dynamically linking related organization models.

    This is particularly useful for custom organizations that can avoid
    multitable inheritence and also add additional attributes to the
    organization users especially.

    The `module_registry` dictionary is used to track the architecture across
    different Django apps. If more than one application makes use of these
    base models, the extended models will share class relationships, which is
    clearly undesirable. This ensures that the relationships between models
    within a module using these base classes are from other organization models.

    """
    module_registry = {}

    def __new__(cls, name, bases, attrs):  # noqa
        # Borrowed from Django-polymorphic
        # Workaround compatibility issue with six.with_metaclass() and custom
        # Django model metaclasses:
        if not attrs and name == 'NewBase':
            return super(OrgMeta, cls).__new__(cls, name, bases, attrs)

        base_classes = ['OrgModel', 'OrgUserModel', 'OrgOwnerModel']
        model = super(OrgMeta, cls).__new__(cls, name, bases, attrs)
        module = model.__module__
        if not cls.module_registry.get(module):
            cls.module_registry[module] = {
                'OrgModel': None,
                'OrgUserModel': None,
                'OrgOwnerModel': None,
            }
        for b in bases:
            key = None
            if b.__name__ in ["AbstractOrganization", "OrganizationBase"]:
                key = 'OrgModel'
            elif b.__name__ in ["AbstractOrganizationUser", "OrganizationUserBase"]:
                key = 'OrgUserModel'
            elif b.__name__ in ["AbstractOrganizationOwner", "OrganizationOwnerBase"]:
                key = 'OrgOwnerModel'
            if key:
                cls.module_registry[module][key] = model

        if all([cls.module_registry[module][klass] for klass in base_classes]):
            model.update_org(module)
            model.update_org_users(module)
            model.update_org_owner(module)

        return model

    def update_org(cls, module):
        """
        Adds the `users` field to the organization model
        """
        try:
            cls.module_registry[module]['OrgModel']._meta.get_field("users")
        except FieldDoesNotExist:
            cls.module_registry[module]['OrgModel'].add_to_class("users",
                models.ManyToManyField(USER_MODEL,
                        through=cls.module_registry[module]['OrgUserModel'].__name__,
                        related_name="%(app_label)s_%(class)s"))

    def update_org_users(cls, module):
        """
        Adds the `user` field to the organization user model and the link to
        the specific organization model.
        """
        try:
            cls.module_registry[module]['OrgUserModel']._meta.get_field("user")
        except FieldDoesNotExist:
            cls.module_registry[module]['OrgUserModel'].add_to_class("user",
                models.ForeignKey(USER_MODEL, related_name="%(app_label)s_%(class)s"))
        try:
            cls.module_registry[module]['OrgUserModel']._meta.get_field("organization")
        except FieldDoesNotExist:
            cls.module_registry[module]['OrgUserModel'].add_to_class("organization",
                models.ForeignKey(cls.module_registry[module]['OrgModel'],
                        related_name="organization_users"))

    def update_org_owner(cls, module):
        """
        Creates the links to the organization and organization user for the owner.
        """
        try:
            cls.module_registry[module]['OrgOwnerModel']._meta.get_field("organization_user")
        except FieldDoesNotExist:
            cls.module_registry[module]['OrgOwnerModel'].add_to_class("organization_user",
                models.OneToOneField(cls.module_registry[module]['OrgUserModel']))
        try:
            cls.module_registry[module]['OrgOwnerModel']._meta.get_field("organization")
        except FieldDoesNotExist:
            cls.module_registry[module]['OrgOwnerModel'].add_to_class("organization",
                models.OneToOneField(cls.module_registry[module]['OrgModel'],
                        related_name="owner"))


class AbstractBaseOrganization(UnicodeMixin, models.Model):
    """
    The umbrella object with which users can be associated.

    An organization can have multiple users but only one who can be designated
    the owner user.
    """

    name = models.CharField(max_length=200,
            help_text=_("The name of the organization"))
    is_active = models.BooleanField(default=True)

    objects = OrgManager()
    active = ActiveOrgManager()

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def user_relation_name(self):
        """
        Returns the string name of the related name to the user.

        This provides a consistent interface across different organization
        model classes.
        """
        return "{0}_{1}".format(self._meta.app_label.lower(),
                self.__class__.__name__.lower())

    def is_member(self, user):
        return True if user in self.users.all() else False


class OrganizationBase(six.with_metaclass(OrgMeta, AbstractBaseOrganization)):
    class Meta(AbstractBaseOrganization.Meta):
        abstract = True


class AbstractBaseOrganizationUser(UnicodeMixin, models.Model):
    """
    ManyToMany through field relating Users to Organizations.

    It is possible for a User to be a member of multiple organizations, so this
    class relates the OrganizationUser to the User model using a ForeignKey
    relationship, rather than a OneToOne relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.
    """

    class Meta:
        abstract = True
        ordering = ['organization', 'user']
        unique_together = ('user', 'organization')

    def __unicode__(self):
        return u"{0} ({1})".format(self.user.get_full_name() if self.user.is_active else
                self.user.email, self.organization.name)

    @property
    def name(self):
        """
        Returns the connected user's full name or string representation if the
        full name method is unavailable (e.g. on a custom user class).
        """
        if hasattr(self.user, 'get_full_name'):
            return self.user.get_full_name()
        return "{0}".format(self.user)


class OrganizationUserBase(six.with_metaclass(OrgMeta, AbstractBaseOrganizationUser)):
    class Meta(AbstractBaseOrganizationUser.Meta):
        abstract = True


class AbstractBaseOrganizationOwner(UnicodeMixin, models.Model):
    """
    Each organization must have one and only one organization owner.
    """

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{0}: {1}".format(self.organization, self.organization_user)


class OrganizationOwnerBase(six.with_metaclass(OrgMeta, AbstractBaseOrganizationOwner)):
    class Meta(AbstractBaseOrganizationOwner.Meta):
        abstract = True

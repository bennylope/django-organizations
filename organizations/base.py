import django

from django.conf import settings
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.base import ModelBase
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from .managers import OrgManager, ActiveOrgManager

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UnicodeMixin(object):
    """
    """
    if six.PY3:
        __str__ = lambda x: x.__unicode__()
    else:
        __str__ = lambda x: unicode(x).encode('utf-8')


class OrgMeta(ModelBase):
    """
    Base metaclass for dynamically linking related organization models.

    This is particularly useful for custom organizations that can avoid
    multitable inheritence and also add additional attributes to the
    organization users, in particular.

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
            if django.VERSION < (1, 5):
                # Let Django fully ignore the class which is inserted in between.
                # Django 1.5 fixed this, see https://code.djangoproject.com/ticket/19688
                attrs['__module__'] = 'django.utils.six'
                attrs['Meta'] = type('Meta', (), {'abstract': True})
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
            if b.__name__ == "OrganizationBase":
                cls.module_registry[module]['OrgModel'] = model
            elif b.__name__ == "OrganizationUserBase":
                cls.module_registry[module]['OrgUserModel'] = model
            elif b.__name__ == "OrganizationOwnerBase":
                cls.module_registry[module]['OrgOwnerModel'] = model

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


class OrganizationBase(six.with_metaclass(OrgMeta, UnicodeMixin, models.Model)):
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

    def is_member(self, user):
        return True if user in self.users.all() else False


class OrganizationUserBase(six.with_metaclass(OrgMeta, UnicodeMixin, models.Model)):
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


class OrganizationOwnerBase(six.with_metaclass(OrgMeta, UnicodeMixin, models.Model)):
    """
    Each organization must have one and only one organization owner.
    """

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{0}: {1}".format(self.organization, self.organization_user)

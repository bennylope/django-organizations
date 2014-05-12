from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models import get_model
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _

from .managers import OrgManager, ActiveOrgManager

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def get_user_model():
    """
    Returns the chosen user model as a class. This functionality is not
    available in Django 1.4.x.
    """
    try:
        klass = get_model(USER_MODEL.split('.')[0], USER_MODEL.split('.')[1])
    except:
        raise ImproperlyConfigured("Your user class, {0},"
                " is improperly defined".format(USER_MODEL))
    return klass


class OrgMeta(ModelBase):
    """
    Base metaclass for dynamically linking related organization models.

    This is particularly useful for custom organizations that can avoid
    multitable inheritence and also add additional attributes to the
    organization users, in particular.

    """
    OrgModel = None
    OrgUserModel = None
    OrgOwnerModel = None

    def __new__(cls, name, bases, attrs):
        model = super(OrgMeta, cls).__new__(cls, name, bases, attrs)
        for b in bases:
            if b.__name__ == "OrganizationBase":
                cls.OrgModel = model
            elif b.__name__ == "OrganizationUserBase":
                cls.OrgUserModel = model
            elif b.__name__ == "OrganizationOwnerBase":
                cls.OrgOwnerModel = model

        if all([cls.OrgModel, cls.OrgUserModel, cls.OrgOwnerModel]):
            model.update_org()
            model.update_org_users()
            model.update_org_owner()

        return model

    def update_org(cls):
        """
        Adds the `users` field to the organization model
        """
        try:
            cls.OrgModel._meta.get_field("users")
        except FieldDoesNotExist:
            cls.OrgModel.add_to_class("users",
                models.ManyToManyField(USER_MODEL, through=cls.OrgUserModel.__name__))

    def update_org_users(cls):
        """
        Adds the `user` field to the organization user model and the link to
        the specific organization model.
        """
        try:
            cls.OrgUserModel._meta.get_field("user")
        except FieldDoesNotExist:
            cls.OrgUserModel.add_to_class("user",
                models.ForeignKey(USER_MODEL, related_name="organization_users"))
        try:
            cls.OrgUserModel._meta.get_field("organization")
        except FieldDoesNotExist:
            cls.OrgUserModel.add_to_class("organization",
                models.ForeignKey(cls.OrgModel, related_name="organization_users"))

    def update_org_owner(cls):
        """
        Creates the links to the organization and organization user for the owner.
        """
        try:
            cls.OrgOwnerModel._meta.get_field("organization_user")
        except FieldDoesNotExist:
            cls.OrgOwnerModel.add_to_class("organization_user",
                models.OneToOneField(cls.OrgUserModel))
        try:
            cls.OrgOwnerModel._meta.get_field("organization")
        except FieldDoesNotExist:
            cls.OrgOwnerModel.add_to_class("organization",
                models.OneToOneField(cls.OrgModel, related_name="owner"))


class OrganizationBase(models.Model):
    """
    The umbrella object with which users can be associated.

    An organization can have multiple users but only one who can be designated
    the owner user.

    """
    __metaclass__ = OrgMeta

    name = models.CharField(max_length=200,
            help_text=_("The name of the organization"))
    is_active = models.BooleanField(default=True)

    objects = OrgManager()
    active = ActiveOrgManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def is_member(self, user):
        return True if user in self.users.all() else False

    def is_admin(self, user):
        return True if self.organization_users.filter(user=user, is_admin=True) else False


class OrganizationUserBase(models.Model):
    """
    ManyToMany through field relating Users to Organizations.

    It is possible for a User to be a member of multiple organizations, so this
    class relates the OrganizationUser to the User model using a ForeignKey
    relationship, rather than a OneToOne relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.

    """
    __metaclass__ = OrgMeta

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active else
                self.user.email, self.organization.name)


class OrganizationOwnerBase(models.Model):
    """Each organization must have one and only one organization owner."""
    __metaclass__ = OrgMeta

    class Meta:
        abstract = True

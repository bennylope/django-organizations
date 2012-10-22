from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import permalink, get_model
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from organizations.managers import OrgManager, ActiveOrgManager


def get_user_model():
    """Returns the User model which should be used. This functionality won't be
    built-in until Django 1.5.
    """
    klass_string = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    try:
        klass = get_model(klass_string.split('.')[0],
                klass_string.split('.')[1])
    except:
        raise ImproperlyConfigured(_("Your user class is improperly defined"))
    return klass


class Organization(TimeStampedModel):
    """The umbrella object with which users can be associated.

    An organization can have multiple users but only one who can be designated
    the owner user.

    """
    name = models.CharField(max_length=100,
            help_text=_("The name of the organization"))
    slug = AutoSlugField(max_length=100, blank=False, editable=True,
            populate_from='name', unique=True,
            help_text=_("The name in all lowercase, suitable for URL identification"))
    users = models.ManyToManyField(get_user_model(), through="OrganizationUser")
    is_active = models.BooleanField(default=True)

    objects = OrgManager()
    active = ActiveOrgManager()

    class Meta:
        ordering = ['name']
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('organization_detail', (), {'organization_pk': self.pk})

    def add_user(self, user, is_admin=False):
        """Adds a new user and if the first user makes the user an admin and
        the owner.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True
        org_user = OrganizationUser.objects.create(user=user,
                organization=self, is_admin=is_admin)
        if users_count == 0:
            OrganizationOwner.objects.create(organization=self,
                    organization_user=org_user)
        return org_user

    def is_member(self, user):
        return True if user in self.users.all() else False

    def is_admin(self, user):
        return True if self.organization_users.filter(user=user, is_admin=True) else False


class OrganizationUser(TimeStampedModel):
    """ManyToMany through field relating Users to Organizations.

    It is possible for a User to be a member of multiple organizations, so this
    class relates the OrganizationUser to the User model using a ForeignKey
    relationship, rather than a OneToOne relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.

    """
    user = models.ForeignKey(get_user_model(), related_name="organization_users")
    organization = models.ForeignKey(Organization,
            related_name="organization_users")
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['organization', 'user']
        unique_together = ('user', 'organization')
        verbose_name = _("organization user")
        verbose_name_plural = _("organization users")

    def __unicode__(self):
        return "%s@%s" % (self.name if self.user.is_active else self.user.email, self.organization.name)

    def delete(self, using=None):
        """
        If the organization user is also the owner, this should not be deleted
        unless it's part of a cascade from the Organization.
        """
        from organizations.exceptions import OwnershipRequired
        if self.organization.owner.organization_user.id == self.id:
            raise OwnershipRequired(_("Cannot delete organization owner before organization or transferring ownership."))
        else:
            super(OrganizationUser, self).delete(using=using)

    @permalink
    def get_absolute_url(self):
        return ('organization_user_detail', (),
                {'organization_pk': self.organization.pk, 'user_pk': self.user.pk})

    @property
    def name(self):
        if hasattr(self.user, 'get_full_name'):
            return self.user.get_full_name()
        return "{0}".format(self.user)


class OrganizationOwner(TimeStampedModel):
    """Each organization must have one and only one organization owner."""

    organization = models.OneToOneField(Organization, related_name="owner")
    organization_user = models.OneToOneField(OrganizationUser,
            related_name="owned_organization")

    class Meta:
        verbose_name = _("organization owner")
        verbose_name_plural = _("organization owners")

    def __unicode__(self):
        return u"{0}: {1}".format(self.organization, self.organization_user)

    def save(self, *args, **kwargs):
        """Extends the default save method by verifying that the chosen
        organization user is associated with the organization.

        """
        from organizations.exceptions import OrganizationMismatch
        if self.organization_user.organization != self.organization:
            raise OrganizationMismatch
        else:
            super(OrganizationOwner, self).save(*args, **kwargs)

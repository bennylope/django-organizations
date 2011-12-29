from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.managers import AccountManager


class Account(models.Model):
    """
    This is the umbrella object under which all account users fall.

    The class has multiple account users and one that is designated the account
    owner.
    """
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, blank=True, null=True,
            unique=True)
    domain = models.CharField(max_length=100, blank=True, null=True,
            unique=True)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    class Meta:
        ordering = ['name']
        verbose_name = _("Account group")
        verbose_name_plural = _("Account groups")

    def __unicode__(self):
        return u"%s" % self.name


class AccountUser(models.Model):
    """
    This relates a User object to the account group. It is possible for a User
    to be a member of multiple accounts, so this class relates the AccountUser
    to the User model using a ForeignKey relationship, rather than a OneToOne
    relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.
    """
    user = models.ForeignKey(User, related_name="accountusers")
    account = models.ForeignKey(Account, related_name="users")
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['account', 'user']
        verbose_name = _("Account user")
        verbose_name_plural = _("Account users")

    def __unicode__(self):
        return u"%s" % self.user

    def delete(self, using=None):
        """
        If the account user is also the owner, this should not be deleted
        unless it's part of a cascade from the Account.
        """
        from accounts.exceptions import OwnershipRequired
        if self.account.owner.id == self.id:
            raise OwnershipRequired("Cannot delete account owner before"
                                    "account or transferring ownership")
        else:
            super(AccountUser, self).delete(using=using)


class AccountOwner(models.Model):
    """
    Each account must have one and only one account owner.
    """
    account = models.OneToOneField(Account, related_name="owner")
    account_user = models.OneToOneField(AccountUser, related_name="owned_accounts")

    class Meta:
        verbose_name = _("Account owner")
        verbose_name_plural = _("Account owners")

    def __unicode__(self):
        return u"%s: %s" % (self.account, self.account_user)

    def save(self, *args, **kwargs):
        """
        Ensure that the account owner is actually an account user
        """
        from accounts.exceptions import AccountMismatch
        if self.account_user.account != self.account:
            raise AccountMismatch
        else:
            super(AccountOwner, self).save(*args, **kwargs)


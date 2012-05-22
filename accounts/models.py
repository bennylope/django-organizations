from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.managers import AccountManager


class AccountsBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(AccountsBase):
    """
    This is the umbrella object under which all account users fall.

    The class has multiple account users and one that is designated the account
    owner.
    """
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through="AccountUser")
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    class Meta:
        ordering = ['name']
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __unicode__(self):
        return u"%s" % self.name

    @permalink
    def get_absolute_url(self):
        return ('account_detail', (), {'account_pk': self.pk})

    def change_owner(self, account_user):
        self.owner.account_user = account_user
        self.owner.save()

    def is_member(self, user):
        return True if self.users.filter(user=user) else False

    def is_admin(self, user):
        return True if self.users.filter(user=user, is_admin=True) else False


class AccountUser(AccountsBase):
    """
    This relates a User object to the account group. It is possible for a User
    to be a member of multiple accounts, so this class relates the AccountUser
    to the User model using a ForeignKey relationship, rather than a OneToOne
    relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.
    """
    user = models.ForeignKey(User, related_name="account_users")
    account = models.ForeignKey(Account, related_name="account_users")
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['account', 'user']
        #unique_together = ('user', 'account') # TODO remove, redundant
        verbose_name = _("account user")
        verbose_name_plural = _("account users")

    def __unicode__(self):
        return u"%s" % self.user

    def delete(self, using=None):
        """
        If the account user is also the owner, this should not be deleted
        unless it's part of a cascade from the Account.
        """
        from accounts.exceptions import OwnershipRequired
        if self.account.owner.id == self.id:
            raise OwnershipRequired(_("Cannot delete account owner before account or transferring ownership"))
        else:
            super(AccountUser, self).delete(using=using)

    @permalink
    def get_absolute_url(self):
        return ('account_user_detail', (),
                {'account_pk': self.account.pk, 'account_user_pk': self.pk})

    @property
    def full_name(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)


class AccountOwner(AccountsBase):
    """
    Each account must have one and only one account owner.
    """
    account = models.OneToOneField(Account, related_name="owner")
    account_user = models.OneToOneField(AccountUser, related_name="owned_accounts")

    class Meta:
        verbose_name = _("account owner")
        verbose_name_plural = _("account owners")

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

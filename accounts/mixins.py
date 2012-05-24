from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account, AccountUser


class AccountMixin(object):
    model = Account
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        kwargs.update({'account': self.account})
        return kwargs

    def get_object(self, **kwargs):
        if hasattr(self, 'account'):
            return self.account
        account_pk = self.kwargs.get('account_pk', None)
        self.account = get_object_or_404(Account, pk=account_pk)
        return self.account
    get_account = get_object # Now available when `get_object` is overridden


class AccountUserMixin(AccountMixin):
    model = AccountUser
    context_object_name = 'account_user'

    def get_context_data(self, **kwargs):
        kwargs = super(AccountUserMixin, self).get_context_data(**kwargs)
        kwargs.update({'account_user': self.object,
            'account': self.object.account})
        return kwargs

    def get_object(self, **kwargs):
        """ Returns the AccountUser object based on the primary keys for both
        the account and the account user.
        """
        if hasattr(self, 'account_user'):
            return self.account_user
        account_pk = self.kwargs.get('account_pk', None)
        account_user_pk = self.kwargs.get('account_user_pk', None)
        self.account_user = get_object_or_404(
                AccountUser.objects.select_related(),
                pk=account_user_pk, account__pk=account_pk)
        return self.account_user


class MembershipRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.account = self.get_account(**kwargs)
        if not self.account.is_member(request.user):
            return HttpResponseForbidden(_("Whoops, wrong account"))
        return super(MembershipRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class AdminRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.account = self.get_account(**kwargs)
        if not self.account.is_admin(request.user):
            return HttpResponseForbidden(_("Sorry, admins only"))
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class OwnerRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.account = self.get_account(**kwargs)
        if self.account.owner.account_user.user != request.user:
            return HttpResponseForbidden(_("You are not the account owner"))
        return super(OwnerRequiredMixin, self).dispatch(request, *args,
                **kwargs)

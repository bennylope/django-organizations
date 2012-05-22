from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account, AccountUser


class AccountMixin(object):
    model = Account
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        return kwargs

    def get_object(self, **kwargs):
        if hasattr(self, 'account'):
            return self.account
        account_pk = self.kwargs.get('account_pk', None)
        self.account = get_object_or_404(Account, pk=account_pk)
        return self.account
    get_account = get_object # Now it's available when the method is overridden


class AccountUserMixin(AccountMixin):
    model = AccountUser
    context_object_name = 'account_user'

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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.account = self.object.account
        context = self.get_context_data(accountuser=self.object,
                account=self.account)
        return self.render_to_response(context)


class MembershipRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        if not self.account.is_member(request.user):
            return HttpResponseForbidden(_("Whoops, wrong account"))
        return super(MembershipRequiredMixin, self).dispatch(self, request, *args,
                **kwargs)


class AdminRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        if not self.account.is_admin(request.user):
            return HttpResponseForbidden(_("Sorry, admins only"))
        return super(AdminRequiredMixin, self).dispatch(self, request, *args,
                **kwargs)


class OwnerRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""
    def dispatch(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        if self.account.owner.account_user.user != request.user:
            return HttpResponseForbidden(_("You are not the account owner"))
        return super(OwnerRequiredMixin, self).dispatch(self, request, *args,
                **kwargs)

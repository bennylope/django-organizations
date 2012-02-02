from django.core.urlresolvers import reverse
from django.views.generic import (ListView, DetailView, CreateView,
        UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from accounts.models import Account, AccountUser


class AccountSingleObjectMixin(object):

    def get_account(self, **kwargs):
        account_pk = self.kwargs.get('account_pk', None)
        return get_object_or_404(Account, id=account_pk)

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request, **kwargs):
        # Use self.object rather than a descriptive name because the
        # get_template_name method looks for that attribute
        self.object= self.get_account(**kwargs)
        context = self.get_context_data(account=self.object)
        return self.render_to_response(context)


class AccountUserSingleObjectMixin(AccountSingleObjectMixin):

    def get_accountuser(self, **kwargs):
        account_pk = self.kwargs.get('account_pk', None)
        accountuser_pk = self.kwargs.get('accountuser_pk', None)
        return get_object_or_404(AccountUser, id=accountuser_pk,
                account__id=account_pk)

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request, **kwargs):
        self.account = self.get_account(**kwargs)
        self.object = self.get_accountuser(**kwargs)
        context = self.get_context_data(accountuser=self.object,
                account=self.account)
        return self.render_to_response(context)


class BaseAccountList(ListView):
    """
    List all documents for all clients

    Filter by category, client
    """
    model = Account
    context_object_name = "accounts"


class BaseAccountDetail(AccountSingleObjectMixin, DetailView):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    pass


class BaseAccountCreate(CreateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = Account


class BaseAccountUpdate(AccountSingleObjectMixin, UpdateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


class BaseAccountDelete(AccountSingleObjectMixin, DeleteView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """

    def get_success_url(self):
        return reverse("account_list")


class BaseAccountUserList(ListView):
    """
    List all users for a given account
    """
    model = AccountUser


class BaseAccountUserDetail(AccountUserSingleObjectMixin, DetailView):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    pass


class BaseAccountUserCreate(CreateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = AccountUser


class BaseAccountUserUpdate(AccountUserSingleObjectMixin, UpdateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


class BaseAccountUserDelete(AccountUserSingleObjectMixin, DeleteView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """

    def get_success_url(self):
        return reverse("accountuser_list")

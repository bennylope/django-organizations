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

    def get(self, request, **kwargs):
        self.account = self.get_account(**kwargs)
        return self.render_to_response({
            "account": self.account,
        })


class AccountUserSingleObjectMixin(AccountSingleObjectMixin):

    def get_accountuser(self, **kwargs):
        account_pk = self.kwargs.get('account_pk', None)
        accountuser_pk = self.kwargs.get('accountuser_pk', None)
        return get_object_or_404(AccountUser, id=accountuser_pk,
                account__id=account_pk)

    def get(self, request, **kwargs):
        self.account = self.get_account(**kwargs)
        self.accountuser = self.get_accountuser(**kwargs)
        return self.render_to_response({
            "account": self.account,
            "accountuser": self.accountuser,
        })


class BaseAccountList(ListView):
    """
    List all documents for all clients

    Filter by category, client
    """
    model = Account


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
    pass


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
    pass



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
    pass


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

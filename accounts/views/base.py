from django.core.urlresolvers import reverse
from django.http import Http404
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
        """
        Using select_related here allows us to make one database call to fetch
        matching user and account information
        """
        account_pk = self.kwargs.get('account_pk', None)
        accountuser_pk = self.kwargs.get('accountuser_pk', None)
        try:
            return AccountUser.objects.select_related().get(pk=accountuser_pk,
                    account__pk=account_pk)
        except AccountUser.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request, **kwargs):
        self.object = self.get_accountuser(**kwargs)
        self.account = self.object.account
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


class BaseAccountUserList(AccountSingleObjectMixin, ListView):
    """
    List all users for a given account
    """
    model = AccountUser
    context_object_name = "accountusers"

    def get(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        self.object_list = self.get_queryset().filter(account=self.account)
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(accountusers=self.object_list,
                account=self.account)
        return self.render_to_response(context)


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

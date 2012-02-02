from django.core.urlresolvers import reverse
from django.views.generic import (ListView, DetailView, CreateView,
        UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import Account, AccountUser



class AccountList(ListView):
    """
    List all documents for all clients

    Filter by category, client
    """
    model = Account
    context_object_name = "documents"
    template_name = "documents/document_list.html"

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(AccountList, self).dispatch(request, *args, **kwargs)


class AccountDetail(DetailView):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    model = Account

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(AccountDetail, self).dispatch(request, *args, **kwargs)


class AccountCreate(CreateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = Account


class AccountUpdate(UpdateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = Account


class AccountDelete(DeleteView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = Account

    def get_success_url(self):
        return reverse("account_list")


class AccountUserList(ListView):
    """
    List all users for a given account
    """
    model = AccountUser

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(AccountUserList, self).dispatch(request, *args, **kwargs)


class AccountUserDetail(DetailView):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    model = AccountUser

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(AccountUserDetail, self).dispatch(request, *args, **kwargs)


class AccountUserCreate(CreateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = AccountUser


class AccountUserUpdate(UpdateView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = AccountUser


class AccountUserDelete(DeleteView):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    model = AccountUser

    def get_success_url(self):
        return reverse("account_list")



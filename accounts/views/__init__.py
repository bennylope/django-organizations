from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from accounts.views.base import (BaseAccountList, BaseAccountDetail,
        BaseAccountUpdate, BaseAccountDelete, BaseAccountCreate,
        BaseAccountUserList, BaseAccountUserDetail, BaseAccountUserUpdate,
        BaseAccountUserCreate, BaseAccountUserDelete)


class AccountList(BaseAccountList):
    """
    List all documents for all clients

    Filter by category, client
    """
    pass


class AccountDetail(BaseAccountDetail):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    pass


class AccountCreate(BaseAccountCreate):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


class AccountUpdate(BaseAccountUpdate):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


class AccountDelete(BaseAccountDelete):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


class AccountUserList(BaseAccountUserList):
    """
    List all users for a given account
    """
    pass


class AccountUserDetail(BaseAccountUserDetail):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    pass


class AccountUserCreate(BaseAccountUserCreate):
    """
    This view should be restricted to the user or admin users
    """
    pass


class AccountUserUpdate(BaseAccountUserUpdate):
    """
    This view should be restricted to the user or admin users
    """
    pass


class AccountUserDelete(BaseAccountUserDelete):
    """
    This view should be restricted to the user or admin users
    """
    pass


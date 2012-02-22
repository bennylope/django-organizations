from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from accounts.decorators import require_account, require_admin, require_owner
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


@require_account
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


@require_admin
class AccountUpdate(BaseAccountUpdate):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


@require_owner
class AccountDelete(BaseAccountDelete):
    """
    This is a view restricted to providers. The data displayed in the form and
    the data pulled back in the from must correspond to the user's provider
    account.
    """
    pass


@require_account
class AccountUserList(BaseAccountUserList):
    """
    List all users for a given account
    """
    pass


@require_admin
class AccountUserDetail(BaseAccountUserDetail):
    """
    View to show information about a document, contingent on the user having
    access to the document.

    Also provides base view fucntionality to the file view.
    """
    pass


@require_admin
class AccountUserCreate(BaseAccountUserCreate):
    """
    This view should be restricted to the user or admin users
    """
    pass


@require_admin
class AccountUserUpdate(BaseAccountUserUpdate):
    """
    This view should be restricted to the user or admin users
    """
    pass


@require_admin
class AccountUserDelete(BaseAccountUserDelete):
    """
    This view should be restricted to the user or admin users
    """
    pass



from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from accounts.models import Account, AccountUser


class AccountAuthMixin(object):
    """
    Class based view mixin to require authentication
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                    self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)


class AccountSingleObjectMixin(AccountAuthMixin):
    """
    Custom get_object method used in order to allow more descriptive keyword
    names in the URL patterns
    """

    model = Account
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        return kwargs

    def get_object(self, **kwargs):
        if hasattr(self, 'object'):
            return self.object
        account_pk = kwargs.get('account_pk', None)
        return get_object_or_404(Account, id=account_pk)
    get_account = get_object


class AccountUserSingleObjectMixin(AccountSingleObjectMixin):

    model = AccountUser
    context_object_name = 'accountuser'

    def get_object(self, **kwargs):
        """
        Returns the AccountUser object based on the primary keys for both the
        account and the account user.
        """
        account_pk = self.kwargs.get('account_pk', None)
        accountuser_pk = self.kwargs.get('accountuser_pk', None)
        try:
            return AccountUser.objects.select_related().get(pk=accountuser_pk,
                    account__pk=account_pk)
        except AccountUser.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.account = self.object.account
        context = self.get_context_data(accountuser=self.object,
                account=self.account)
        return self.render_to_response(context)


class AccountsUpdateMixin(object):
    """
    Ensure that the form is present in Update views
    """
    def get_context_data(self, **kwargs):
        context = super(AccountsUpdateMixin, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        return context


class AccountUserOnly(object):
    """
    A mixin to restrict the view to members of the given account
    """
    pass


class AdminUserOnly(object):
    """
    A mixin to restrict the view to admin members of the given account only
    """
    pass


class OwnerUserOnly(object):
    """
    A mixin to restrict the view to the owner of the account only
    """
    pass

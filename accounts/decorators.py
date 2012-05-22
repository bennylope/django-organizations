from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator

from accounts.models import AccountUser


def require_account(original_class):
    orig_dispatch = original_class.dispatch

    # TODO: use alternative to login_required being called here and in
    # base dispatch method
    @method_decorator(login_required)
    def new_dispatch(self, request, *args, **kwargs):
        self.object = self.get_account(**kwargs)
        user = AccountUser.objects.filter(user=request.user, account=self.object)
        if not user:
            return HttpResponseForbidden(_("Only account members can view this page."))
        return orig_dispatch(self, request, *args, **kwargs)

    original_class.dispatch = new_dispatch # set the class' dispatch to the new method
    return original_class


def require_admin(original_class):
    orig_dispatch = original_class.dispatch

    @method_decorator(login_required)
    def new_dispatch(self, request, *args, **kwargs):
        self.object = self.get_account(**kwargs)
        try:
            user = AccountUser.objects.get(user=request.user, account=self.object)
        except AccountUser.DoesNotExist:
            pass
        else:
            if user.is_admin:
                return orig_dispatch(self, request, *args, **kwargs)
        return HttpResponseForbidden(_("Only account admins can view this page."))

    original_class.dispatch = new_dispatch # set the class' dispatch to the new method
    return original_class


def require_owner(original_class):
    orig_dispatch = original_class.dispatch

    @method_decorator(login_required)
    def new_dispatch(self, request, *args, **kwargs):
        self.object = self.get_account(**kwargs)
        if request.user != self.object.owner.account_user.user:
            return HttpResponseForbidden(_("Only account members can view this page."))
        return orig_dispatch(self, request, *args, **kwargs)

    original_class.dispatch = new_dispatch # set the class' dispatch to the new method
    return original_class


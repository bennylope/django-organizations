from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import login as login_view
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import (View, ListView, DetailView, UpdateView,
        CreateView, DeleteView, FormView)

from accounts.models import Account
from accounts.mixins import (AccountMixin, AccountUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)
from accounts.forms import (LoginForm, AccountForm, AccountUserForm,
        AccountUserAddForm, AccountAddForm, UserProfileForm)
from accounts.invitations.backends import InvitationBackend


class LoginView(FormView):
    """
    Performs the same actions as the default Django login view but also
    checks for a logged in user and redirects that person if s/he is
    logged in.
    """
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        redirect_url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect_url)
        else:
            form = LoginForm(initial={"redirect_url": redirect_url})
            return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        return login_view(request, redirect_field_name="redirect_url",
                authentication_form=LoginForm)


class LogoutView(View):
    """
    Logs the user out, and then redirects to the login view. It also
    updates the request messages with a message that the user has 
    successfully logged out.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, "You have successfully logged out.")
        return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class BaseAccountList(ListView):
    model = Account
    context_object_name = "accounts"

    def get_queryset(self):
        return super(BaseAccountList,
                self).get_queryset().filter(users=self.request.user)


class BaseAccountDetail(AccountMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(BaseAccountDetail, self).get_context_data(**kwargs)
        context['account_users'] = self.account.account_users.all()
        context['account'] = self.account
        return context


class BaseAccountCreate(CreateView):
    model = Account
    form_class = AccountAddForm
    template_name = 'accounts/account_form.html'

    def get_success_url(self):
        return reverse("account_list")

    def get_form_kwargs(self):
        kwargs = super(BaseAccountCreate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseAccountUpdate(AccountMixin, UpdateView):
    form_class = AccountForm

    def get_form_kwargs(self):
        kwargs = super(BaseAccountUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseAccountDelete(AccountMixin, DeleteView):
    def get_success_url(self):
        return reverse("account_list")


class BaseAccountUserList(AccountMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        self.object_list = self.account.account_users.all()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(account_users=self.object_list,
                account=self.account)
        return self.render_to_response(context)


class BaseAccountUserDetail(AccountUserMixin, DetailView):
    pass


class BaseAccountUserCreate(AccountMixin, CreateView):
    form_class = AccountUserAddForm
    template_name = 'accounts/accountuser_form.html'

    def get_success_url(self):
        return reverse('account_user_list',
                kwargs={'account_pk': self.object.account.pk})

    def get_form_kwargs(self):
        kwargs = super(BaseAccountUserCreate, self).get_form_kwargs()
        kwargs.update({'account': self.account, 'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.account = self.get_object()
        return super(BaseAccountUserCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.account = self.get_object()
        return super(BaseAccountUserCreate, self).post(request, *args, **kwargs)


class BaseAccountUserRemind(AccountUserMixin, DetailView):
    template_name = 'accounts/accountuser_remind.html'

    def get_object(self, **kwargs):
        self.account_user = super(BaseAccountUserRemind, self).get_object()
        if self.account_user.user.is_active:
            raise Http404(_("Already active")) # TODO add better error
        return self.account_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        InvitationBackend().send_reminder(self.object.user,
                **{'domain': get_current_site(self.request),
                    'account': self.account, 'sender': request.user})
        return HttpResponseRedirect(self.object.get_absolute_url())


class BaseAccountUserUpdate(AccountUserMixin, UpdateView):
    form_class = AccountUserForm


class BaseAccountUserDelete(AccountUserMixin, DeleteView):
    def get_success_url(self):
        return reverse("accountuser_list")


class AccountList(BaseAccountList):
    pass


class AccountCreate(BaseAccountCreate):
    pass


class AccountDetail(MembershipRequiredMixin, BaseAccountDetail):
    pass


class AccountUpdate(AdminRequiredMixin, BaseAccountUpdate):
    pass


class AccountDelete(OwnerRequiredMixin, BaseAccountDelete):
    pass


class AccountUserList(MembershipRequiredMixin, BaseAccountUserList):
    pass


class AccountUserDetail(AdminRequiredMixin, BaseAccountUserDetail):
    pass


class AccountUserUpdate(AdminRequiredMixin, BaseAccountUserUpdate):
    pass


class AccountUserCreate(AdminRequiredMixin, BaseAccountUserCreate):
    pass


class AccountUserRemind(AdminRequiredMixin, BaseAccountUserRemind):
    pass


class AccountUserDelete(AdminRequiredMixin, BaseAccountUserDelete):
    pass


class UserProfileView(UpdateView):
    form_class = UserProfileForm
    template_name = "accounts/accountuser_form.html"

    def get_success_url(self):
        success_url = getattr(self, 'success_url')
        return success_url if success_url else reverse('user_profile')

    def get_object(self, **kwargs):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(UserProfileView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile'] = True
        return context

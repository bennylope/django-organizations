
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import login as login_view
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import (View, ListView, DetailView, UpdateView, DeleteView,
        FormView)
from django.utils.decorators import method_decorator

from accounts.forms import LoginForm
from accounts.models import Account
from accounts.mixins import AccountMixin, AccountUserMixin
from accounts.forms import (AccountUserForm, AccountUserAddForm,
        AccountAddForm, ProfileUserForm)


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


class BaseAccountDetail(AccountMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(BaseAccountDetail, self).get_context_data(**kwargs)
        context['account_users'] = self.account.users.all()
        context['account'] = self.account
        return context


class BaseAccountCreate(FormView):
    form_class = AccountAddForm
    template_name = 'accounts/account_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(BaseAccountCreate, self).form_valid(form)


class BaseAccountUpdate(AccountMixin, UpdateView):
    pass


class BaseAccountDelete(AccountMixin, DeleteView):
    def get_success_url(self):
        return reverse("account_list")


class BaseAccountUserList(AccountMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.account = self.get_account(**kwargs)
        self.object_list = self.account.users.all()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(account_users=self.object_list,
                account=self.account)
        return self.render_to_response(context)


class BaseAccountUserDetail(AccountUserMixin, DetailView):
    pass


class BaseAccountUserCreate(AccountMixin, FormView):
    form_class = AccountUserAddForm
    template_name = 'accounts/accountuser_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """
        Create the User object, then the AccountUser object, then return the
        user to the account page
        """
        form.save(self.object)
        return super(BaseAccountUserCreate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form,
            account=self.object))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BaseAccountUserUpdate(AccountUserMixin,
        UpdateView):
    form_class = AccountUserForm


class BaseAccountUserDelete(AccountUserMixin, DeleteView):
    def get_success_url(self):
        return reverse("accountuser_list")


class AccountList(BaseAccountList):
    pass


class AccountDetail(BaseAccountDetail):
    pass


class AccountUpdate(BaseAccountUpdate):
    pass


class AccountDelete(BaseAccountDelete):
    pass


class AccountCreate(BaseAccountCreate):
    pass


class AccountUserList(BaseAccountUserList):
    pass


class AccountUserDetail(BaseAccountUserDetail):
    pass


class AccountUserUpdate(BaseAccountUserUpdate):
    pass


class AccountUserCreate(BaseAccountUserUpdate):
    pass


class AccountUserDelete(BaseAccountUserDelete):
    pass


class UserProfileView(FormView):
    form_class = ProfileUserForm
    template_name = "accounts/accountuser_form.html"
    success_url = "/"

    def success_redirect(self, referrer):
        return HttpResponseRedirect(referrer or self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile'] = True
        return context

    def form_valid(self, form):
        """
        Saves updates to the User model
        """
        # Save the user
        self.user.username = form.cleaned_data['username']
        self.user.first_name = form.cleaned_data['first_name']
        self.user.last_name = form.cleaned_data['last_name']
        self.user.email = form.cleaned_data['email']
        if form.cleaned_data['password1']:
            self.user.set_password(form.cleaned_data['password1'])
        self.user.save()
        return self.success_redirect(form.cleaned_data['referrer'])

    def get(self, request, *args, **kwargs):
        self.referrer = request.META.get('HTTP_REFERER')
        self.user = request.user
        form = ProfileUserForm(initial={
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'referrer': self.referrer,})
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.user = request.user
        return super(UserProfileView, self).post(request, *args, **kwargs)


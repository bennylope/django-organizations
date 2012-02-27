from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import login as login_view
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, FormView

from accounts.forms import LoginForm


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


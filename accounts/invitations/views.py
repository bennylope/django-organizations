from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView

from accounts.invitations.forms import InvitationRegistrationForm
from accounts.invitations.tokens import InvitationTokenGenerator


class RegisterInvite(UpdateView):
    model = User
    form_class = InvitationRegistrationForm
    template_name = "invitations/register_form.html"

    def get_success_url(self):
        return "/accounts/"

    def get_form_kwargs(self):
        kwargs = super(RegisterInvite, self).get_form_kwargs()
        # The current username is a UUID, don't display it
        kwargs.update({'initial': {'username': ''}})
        return kwargs

    def get_object(self):
        """
        Always checks token even if no matching user id. Hey, no timing
        attacks.
        """
        user_id = self.kwargs.get('user_id')
        token = self.kwargs.get('token')
        try:
            user = User.objects.get(id=user_id, is_active=False)
        except User.DoesNotExist:
            user = User.objects.none()
        if InvitationTokenGenerator().check_token(user, token):
            return user
        raise Http404(_("Your URL may have expired."))

    def form_valid(self, form):
        form.instance.is_active = True
        return super(RegisterInvite, self).form_valid(form)

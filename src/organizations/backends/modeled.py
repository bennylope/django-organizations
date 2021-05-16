# -*- coding: utf-8 -*-

"""
Invitations that use an invitation model
"""
import email.utils
from typing import List  # noqa
from typing import Optional  # noqa
from typing import Text  # noqa
from typing import Tuple  # noqa

from django.conf import settings
from django.contrib.auth.models import AbstractUser  # noqa
from django.core.mail import EmailMessage
from django.http import HttpRequest  # noqa
from django.http import HttpResponse  # noqa
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import path
from django.utils.translation import gettext_lazy as _

from organizations.backends.defaults import InvitationBackend
from organizations.backends.forms import UserRegistrationForm
from organizations.base import AbstractBaseOrganization  # noqa
from organizations.base import OrganizationInvitationBase  # noqa


class ModelInvitation(InvitationBackend):
    """Invitation backend for model-tracked invitations"""

    notification_subject = "organizations/email/notification_subject.txt"
    notification_body = "organizations/email/notification_body.html"
    invitation_subject = "organizations/email/modeled_invitation_subject.txt"
    invitation_body = "organizations/email/modeled_invitation_body.html"
    reminder_subject = "organizations/email/modeled_reminder_subject.txt"
    reminder_body = "organizations/email/modeled_reminder_body.html"
    invitation_join_template = "organizations/invitation_join.html"

    form_class = UserRegistrationForm

    def __init__(self, org_model=None, namespace=None):
        super().__init__(org_model=org_model, namespace=namespace)
        self.invitation_model = (
            self.org_model.invitation_model
        )  # type: OrganizationInvitationBase

    def get_invitation_queryset(self):
        """Return this to use a custom queryset that checks for expiration, for example"""
        return self.invitation_model.objects.all()

    def get_invitation_accepted_url(self):
        """Returns the redirect URL after user accepts invitation"""
        return "/"

    def get_invitation_accepted_registered_url(self):
        """Returns the redirect URL after new user accepts invitation"""
        return self.get_invitation_accepted_url()

    def activation_router(self, request, guid):
        """"""
        invitation = get_object_or_404(self.get_invitation_queryset(), guid=guid)
        if invitation.invitee:
            return redirect(self.get_invitation_accepted_url())

        if request.user.is_authenticated:
            return self.activate_existing_user_view(request, invitation)
        else:
            return self.activate_new_user_view(request, invitation)

    def activate_existing_user_view(self, request, invitation):
        # type: (HttpRequest, OrganizationInvitationBase) -> HttpResponse
        """"""
        if request.user == invitation.invited_by:
            return HttpResponseForbidden(_("This is not your invitation"))
        if request.method == "POST":
            invitation.activate(request.user)
            return redirect(self.get_invitation_accepted_url())
        return render(
            request, self.invitation_join_template, {"invitation": invitation}
        )

    def activate_new_user_view(self, request, invitation):
        # type: (HttpRequest, OrganizationInvitationBase) -> HttpResponse
        """"""
        form = self.get_form(data=request.POST or None)
        if request.method == "POST" and form.is_valid():
            new_user = form.save()  # type: AbstractUser
            invitation.activate(new_user)
            return redirect(self.get_invitation_accepted_registered_url())
        return render(
            request,
            self.registration_form_template,
            {"invitation": invitation, "form": form},
        )

    def get_urls(self):
        # type: () -> List[path]
        return [
            path(
                "<uuid:guid>/", view=self.activation_router, name="invitations_register"
            )
        ]

    @property
    def urls(self):
        # type: () -> Tuple[List[path], Text]
        return self.get_urls(), self.namespace or "registration"

    def invite_by_email(self, email, user, organization, **kwargs):
        """
        Primary interface method by which one user invites another to join

        Args:
            email:
            request:
            **kwargs:

        Returns:
            an invitation instance

        Raises:
            MultipleObjectsReturned if multiple matching users are found

        """
        # TODO(bennylope): verify no such user already?
        # try:
        #     invitee = self.user_model.objects.get(email__iexact=email)
        # except self.user_model.DoesNotExist:
        #     invitee = None

        # TODO allow sending just the OrganizationUser instance
        user_invitation = self.invitation_model.objects.create(
            invitee_identifier=email.lower(),
            invited_by=user,
            organization=organization,
        )
        self.send_invitation(user_invitation)
        return user_invitation

    def send_invitation(self, invitation, **kwargs):
        """
        Sends an invitation message for a specific invitation.

        This could be overridden to do other things, such as sending a confirmation
        email to the sender.

        Args:
            invitation:

        Returns:

        """
        return self.email_message(
            invitation.invitee_identifier,
            self.invitation_subject,
            self.invitation_body,
            invitation.invited_by,
            **kwargs
        ).send()

    def email_message(
        self,
        recipient,  # type: Text
        subject_template,  # type: Text
        body_template,  # type: Text
        sender=None,  # type: Optional[AbstractUser]
        message_class=EmailMessage,
        **kwargs
    ):
        """
        Returns an invitation email message. This can be easily overridden.
        For instance, to send an HTML message, use the EmailMultiAlternatives message_class
        and attach the additional conent.
        """
        from_email = "%s %s <%s>" % (
            sender.first_name,
            sender.last_name,
            email.utils.parseaddr(settings.DEFAULT_FROM_EMAIL)[1],
        )
        reply_to = "%s %s <%s>" % (sender.first_name, sender.last_name, sender.email)

        headers = {"Reply-To": reply_to}
        kwargs.update({"sender": sender, "recipient": recipient})

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)

        subject = subject_template.render(
            kwargs
        ).strip()  # Remove stray newline characters

        body = body_template.render(kwargs)

        return message_class(subject, body, from_email, [recipient], headers=headers)

# -*- coding: utf-8 -*-

# Copyright (c) 2012-2018, Ben Lopatin and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Invitations that use an invitation model
"""
import email.utils
from typing import Optional  # noqa
from typing import Text  # noqa

from django.conf import settings
from django.conf.urls import url
from django.core.mail import EmailMessage
from django.template import loader

from organizations.backends.defaults import InvitationBackend
from organizations.base import OrganizationInvitationBase


class ModelInvitation(InvitationBackend):
    """

    """

    def __init__(self, org_model=None):
        super(ModelInvitation, self).__init__(org_model=org_model)
        self.invitation_model = self.org_model.invitation_model

    def get_urls(self):
        return [
            url(
                r"^(?P<guid>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
                view=self.activate_view,
                name="invitations_register",
            )
        ]

    def invite_by_email(self, email, user, **kwargs):
        # type: (Text, Optional[Request], Any) -> OrganizationInvitationBase
        """

        Args:
            email:
            request:
            **kwargs:

        Returns:
            an invitation instance

        """
        try:
            invitee = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            invitee = None

        user_invitation = self.invitation_model(invitee=invitee, invitee_identifier=email, invited_by=user)
        self.send_invitation(user_invitation)
        return user_invitation

    def send_invitation(self, invitation):
        """

        Args:
            invitation:

        Returns:

        """
        # self.email_message(
        #     user, self.invitation_subject, self.invitation_body, sender, **kwargs
        # ).send()
        return True

    def email_message(
        self,
        user,
        subject_template,
        body_template,
        sender=None,
        message_class=EmailMessage,
        **kwargs
    ):
        """
        Returns an email message for a new user. This can be easily overridden.
        For instance, to send an HTML message, use the EmailMultiAlternatives message_class
        and attach the additional conent.
        """
        from_email = "%s %s <%s>" % (
            sender.first_name,
            sender.last_name,
            email.utils.parseaddr(settings.DEFAULT_FROM_EMAIL)[1],
        )
        reply_to = "%s %s <%s>" % (
            sender.first_name, sender.last_name, sender.email
        )

        headers = {"Reply-To": reply_to}
        kwargs.update({"sender": sender, "user": user})

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)

        subject = subject_template.render(
            kwargs
        ).strip()  # Remove stray newline characters

        body = body_template.render(kwargs)

        return message_class(subject, body, from_email, [user.email], headers=headers)

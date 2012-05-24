import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _

from .tokens import InvitationTokenGenerator


class InvitationBackend(object):
    """
    A default invitation backend
    """
    invitation_subject = 'invitations/invitation_subject.txt'
    invitation_body = 'invitations/invitation_body.html'
    reminder_subject = 'invitations/reminder_subject.txt'
    reminder_body = 'invitations/reminder_body.html'

    def create_invitation(self, email, **kwargs):
        """
        :param email: string representing the invitee's email address
        """
        user = User.objects.create(username=unicode(uuid.uuid1()), email=email,
                password=User.objects.make_random_password())
        user.is_active = False
        user.save()
        token = InvitationTokenGenerator().make_token(user)
        self.send_invitation(user, token, **kwargs)
        return user

    def send_invitation(self, user, token, **kwargs):
        """
        Sends an invitation email to the user.

        :param user: the User to be invited to join
        :param token: a string to form the 
        """
        try:
            from_email = settings.DEFAULT_FROM_EMAIL
        except AttributeError:
            raise ImproperlyConfigured(_("You must define a default email adderess"))

        sender = kwargs.get('sender', None)
        if sender:
            from_email = "%s %s <%s>" % (sender.first_name, sender.last_name,
                    from_email)

        domain = kwargs.get('domain', '')

        c = Context({
            'domain': domain,
            'url': '/register/',
            'user': user,
            'token': unicode(token),
            'protocol': 'http',
            'sender': sender,
            'account': kwargs.get('account', None)
        })

        msg_subject = kwargs.get('subject_template', self.invitation_subject)
        msg_body = kwargs.get('body_template', self.invitation_body)

        subject_template = loader.get_template(msg_subject)
        body_template = loader.get_template(msg_body)
        subject = subject_template.render(c).strip() # Remove newline character
        body = body_template.render(c)
        headers = {'Reply-To': settings.DEFAULT_FROM_EMAIL}
        EmailMessage(subject, body, from_email, [user.email], headers).send()

    def send_reminder(self, user, **kwargs):
        kwargs.update({'subject_template': 'invitations/reminder_subject.txt',
            'body_template': 'invitations/reminder_body.html'})
        token = InvitationTokenGenerator().make_token(user)
        self.send_invitation(user, token, **kwargs)

    def activate(self, request, key):
        raise NotImplementedError

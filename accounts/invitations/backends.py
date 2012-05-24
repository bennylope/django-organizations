import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _

from .tokens import InvitationTokenGenerator


class InvitationBackend(object):
    """
    A default invitation backend
    """

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

        c= Context({
            'url': 'yahoo.com', #TODO replace this
            'user': user,
            'token': u"%s" % token,
            'protocol': 'http',
        })

        subject_template = loader.get_template('invitations/email_subject.txt')
        body_template = loader.get_template('invitations/email_body.html')
        subject = subject_template.render(c).strip() # Remove newline character
        body = body_template.render(c)
        headers = {'Reply-To': settings.DEFAULT_FROM_EMAIL}
        EmailMessage(subject, body, from_email, [user.email], headers).send()

    def send_reminder(self, user):
        raise NotImplementedError

    def activate(self, request, key):
        raise NotImplementedError

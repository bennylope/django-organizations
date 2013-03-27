Invitation and Registration Backends
====================================

The purpose of the backends is to provide scaffolding for adding and managing
users and organizations. **The scope is limited to the basics of adding new
users and creating new organizations**.

While the default backends should suffice for basic implementations, the
backends are designed to be easily extended for your specific project needs. If
you make use of a profile model or a user model other than `auth.User` you
should extend the releveant backends for your own project. If you've used
custom URL names then you'll also want to extend the backends to use your own
success URLs.

You do not have to implement these backends to use django-organizations, but
they will make user management within accounts easier.

The two default backends share a common structure and interface. This includes
methods for sending emails, generating URLs, and template references.

The backend URLs will need to be configured to allow for registration and/or
user activation. You can add these by referring to the backend's `get_urls`
method:::

    from organizations.backends import invitation_backend

    urlpatterns = patterns('',
        url(r'^invitations/', include(invitation_backend().get_urls())),
     )

.. _registration-backend:

Registration Backend
--------------------

The registration backend is used for creating new users with new organizations,
e.g. new user sign up.

Attributes
~~~~~~~~~~

.. attribute:: RegistrationBackend.activation_subject

  Template path for the activation email subject. Default::

      invitation_subject = 'organizations/email/activation_subject.txt'

.. attribute:: RegistrationBackend.activation_body

  Template path for the activation email body. Default::

      invitation_body = 'organizations/email/activation_body.html'

.. attribute:: RegistrationBackend.reminder_subject

  Template path for the reminder email subject. Default::

      reminder_subject = 'organizations/email/reminder_subject.txt'

.. attribute:: RegistrationBackend.reminder_body

  Template path for the reminder email body. Default::

      reminder_body = 'organizations/email/reminder_body.html'

.. attribute:: RegistrationBackend.form_class

  Form class which should be used for activating a user account when
  registering. Default::

      form_class = UserRegistrationForm

.. _invitation-backend:

Invitation backend
------------------

The invitation backend is used for adding new users to an *existing
organization*.

When 

Attributes
~~~~~~~~~~

.. attribute:: InvitationBackend.invitation_subject

  Template path for the invitation email subject. Default::

      invitation_subject = 'organizations/email/invitation_subject.txt'

.. attribute:: InvitationBackend.invitation_body

  Template path for the invitation email body. Default::

      invitation_body = 'organizations/email/invitation_body.html'

.. attribute:: InvitationBackend.reminder_subject

  Template path for the reminder email subject. Default::

      reminder_subject = 'organizations/email/reminder_subject.txt'

.. attribute:: InvitationBackend.reminder_body

  Template path for the reminder email body. Default::

      reminder_body = 'organizations/email/reminder_body.html'

.. attribute:: InvitationBackend.form_class

  Form class which should be used for activating a user account in response to
  an invitation. Default::

      form_class = UserRegistrationForm

Methods
~~~~~~~

The primary methods of interest are the `invite_by_email` method and the
`get_success_url` method.

.. method:: InvitationBackend.get_success_url()

  This method behaves as expected and returns a URL to which the user should be
  redirected after successfully activating an account. By default it returns the
  user to the organization list URL, but can be configured to any URL::

      def get_success_url(self):
          return reverse('my_fave_app')

.. method:: InvitationBackend.invite_by_email(email, sender=None, request=None, **kwargs)

  This is the primary interface method for the invitation backend. This method
  should be referenced from your invitation form or view and if you need to
  customize what happens when a user is invited, this is where to do it.

  Usage example in a form class::

      class AccountUserAddForm(OrganizationUserAddForm):

          class Meta:
              model = OrganizationUser

          def save(self, *args, **kwargs):
              try:
                  user = get_user_model().objects.get(email__iexact=self.cleaned_data['email'])
              except get_user_model().MultipleObjectsReturned:
                  raise forms.ValidationError("This email address has been used multiple times.")
              except get_user_model().DoesNotExist:
                  user = invitation_backend().invite_by_email(
                          self.cleaned_data['email'],
                          **{'domain': get_current_site(self.request),
                              'organization': self.organization})

              return OrganizationUser.objects.create(user=user,
                      organization=self.organization)

  .. note::
    As the example shows, the invitation backend does not associate the
    individual user with the organization account, it only creates the user so it
    can be associated in addition to sending the invitation.

    Use additional keyword arguments passed via `**kwargs` to include
    contextual information in the invitation, such as what account the user is
    being invited to join.

.. method:: InvitationBackend.activate_view(request, user_id, token)

  This method is a view for activating a user account via a unique link sent
  via email. The view ensures the token matches a user and is valid, that the
  user is unregistered, and that the user's entered data is valid (e.g.
  password, names). User entered data is validated against the `form_class`.

  The view then ensures the user's `OrganizationUser` connections are
  activated, logs the user in with the entered credentials and redirects to the
  success URL.

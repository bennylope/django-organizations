========
Settings
========

.. attribute:: settings.INVITATION_BACKEND

  The full dotted path to the invitation backend. Defaults to::

      INVITATION_BACKEND = 'organizations.backends.defaults.InvitationBackend'

.. attribute:: settings.REGISTRATION_BACKEND

  The full dotted path to the regisration backend. Defaults to::

      REGISTRATION_BACKEND = 'organizations.backends.defaults.RegistrationBackend'

.. attribute:: settings.AUTH_USER_MODEL

  This setting is introduced in Django 1.5 to support swappable user models.
  The defined here will be used by django-organizations as the related user
  class to Organizations.

  Though the swappable user model functionality is absent, this setting can be
  used in Django 1.4 with django-organizations to relate a custom user model.
  If undefined it will default to::

      AUTH_USER_MODEL = 'auth.User'

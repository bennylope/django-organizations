from django.conf import settings
from django.contrib.auth.models import User

from organizations.utils import model_field_attr


ORGS_INVITATION_BACKEND = getattr(settings, 'INVITATION_BACKEND',
        'organizations.backends.defaults.InvitationBackend')

ORGS_REGISTRATION_BACKEND = getattr(settings, 'REGISTRATION_BACKEND',
        'organizations.backends.defaults.RegistrationBackend')

ORGS_EMAIL_LENGTH = model_field_attr(User, 'email', 'max_length')

from django.conf import settings


INVITATION_BACKEND = getattr(settings, 'INVITATION_BACKEND',
        'accounts.invitations.backends.InvitationBackend')

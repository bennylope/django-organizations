from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


REGISTRATION_TIMEOUT_DAYS = getattr(settings, 'REGISTRATION_TIMEOUT_DAYS', 15)


class RegistrationTokenGenerator(PasswordResetTokenGenerator):
    """
    Very similar to the password reset token generator, but should
    allow slightly greater time for timeout, so it only updates one
    method, replacing PASSWORD_RESET_TIMEOUT_DAYS from the global
    settings with REGISTRATION_TIMEOUT_DAYS from application
    settings.
    
    Has the additional interface method:
        -- make_token(user): Returns a token that can be used once to do a
                            password reset for the given user.
    """
    
    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # Check the timestamp is within limit
        if (self._num_days(self._today()) - ts) > REGISTRATION_TIMEOUT_DAYS:
            return False

        return True


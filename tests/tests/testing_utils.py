
class AccountUserTestingMixin(object):
    """
    Common setup required for testing accounts
    """

    def create_users(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user("user", "none",
                "user@example.com")
        seconduser = User.objects.create_user("lucy", "none",
                "second@example.com")
        thirduser = User.objects.create_user("bob", "none",
                "third@example.com")
        return user, seconduser, thirduser

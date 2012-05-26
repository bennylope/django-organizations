from django.db import models


class OrganizationManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(is_active=True)

    def get_for_user(self, user):
        """
        Returns all matching `Organization` objects

        user: a `User` object
        """
        return self.get_query_set().filter(users=user)

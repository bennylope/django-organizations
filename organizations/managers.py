from django.db import models


class OrgManager(models.Manager):

    def get_for_user(self, user):
        """
        Returns all matching `Organization` objects

        user: a `User` object
        """
        return self.get_query_set().filter(users=user)



class ActiveOrgManager(OrgManager):
    """
    A more useful extension of the default manager which returns querysets
    including only active organizations
    """

    def get_query_set(self):
        return super(ActiveOrgManager,
                self).get_query_set().filter(is_active=True)

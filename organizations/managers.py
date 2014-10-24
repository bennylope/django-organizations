from django.db import models


class OrgManager(models.Manager):

    def get_for_user(self, user):
        if hasattr(self, 'get_queryset'):
            return self.get_queryset().filter(users=user)
        else:
            # Deprecated method for older versions of Django
            return self.get_query_set().filter(users=user)


class ActiveOrgManager(OrgManager):
    """
    A more useful extension of the default manager which returns querysets
    including only active organizations
    """

    def get_queryset(self):
        try:
            return super(ActiveOrgManager,
                    self).get_queryset().filter(is_active=True)
        except AttributeError:
            # Deprecated method for older versions of Django.
            return super(ActiveOrgManager,
                    self).get_query_set().filter(is_active=True)
    get_query_set = get_queryset

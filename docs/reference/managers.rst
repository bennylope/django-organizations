========
Managers
========

`OrgManager`
============

Base manager class for the `Organization` model.

.. method:: OrgManager.get_for_user(user)

  Returns a QuerySet of Organizations that the given user is a member of.

`ActiveOrgManager`
==================

This manager extends the `OrgManager` class by defining a base queryset
including only active Organizations. This manager is accessible from the
`active` attribute on the `Organization` class.

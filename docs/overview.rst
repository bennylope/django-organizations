Overview
========

django-organizations allows you to add multi-user accounts to your application
and tie permissions and actions to organization level accounts.

The core of the application consists of these three models:

* **Organization** The group object. This is what you would associate your own
  app's functionality with, e.g. subscriptions, repositories, projects, etc.
* **OrganizationUser** A custom `through` model for the ManyToMany relationship
  between the `Organization` model and the `User` model. It stores additional
  information about the user specific to the organization and provides a
  convenient link for organization ownership.
* **OrganizationOwner** The user with rights over the life and death of the
  organization. This is a one to one relationship with the `OrganizationUser`
  model. This allows `User` objects to own multiple organizations and makes it
  easy to enforce ownership from within the organization's membership.

Users and multi-account membership
----------------------------------

.. TODO add image showing how these are all related

The key to these relationships is that while an `OrganizationUser` is
associated with one and only one `Organization`, a `User` can be associated
with multiple `OrganizationUsers` and hence multiple `Organizations`.

.. note::

    This means that the OrganizationUser class cannot be used as a UserProfile
    as that requires a one-to-one relationship with the User class. That is
    better provided by your own project or application.

In your project you can associate accounts with things like subscriptions,
documents, and other shared resources, all of which the account users can then
access.

For many projects a simple one-user-per-account model will suffice, and this
can be handled quite ably in your own application's logic.

Default Views
-------------

Hooking the django-organizations URLs into your project provides a default set
of views for accessing and updating organizations and organization membership.

Implementing in your own project
--------------------------------

While django-organizations has some basic usability 'out-of-the-box', it's
designed to be used as a foundation for project specific functionality. The
view mixins should provide base functionality from which to work for unique
situations.

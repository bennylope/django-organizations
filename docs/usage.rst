Basic Usage
===========

After installing django-organizations you can make basic use of the accounts
with minimal configuration.

The application's default views and URL configuration provide functionality for
account creation, user registration, and account management.

Creating accounts
-----------------

.. note::
    This is a to-do item, and an opportunity to contribute to the project!

User registration
-----------------

You can register new users and organizations through your project's own system
or use the extensible invitation and registration backends.

The default invitation backend accepts an email address and returns the user
who either matches that email address or creates a new user with that email
address. The view for adding a new user is then responsbile for adding this
user to the organization.

The `OrganizationSignup` view is used for allowing a user new to the site to
create an organization and account. This view relies on the registration
backend to create and verify a new user.

The backends can be extended to fit the needs of a given site.

Creating accounts
~~~~~~~~~~~~~~~~~

When a new user signs up to create an account - meaning a new UserAccount for a
new Account - the view creates a new `User`, a new `Account`, a new
`AccountUser`, and a new `AccountOwner` object linking the newly created
`Account` and `AccountUser`.

Adding users
~~~~~~~~~~~~

The user registration system in django-organizations is based on the same
token generating mechanism as Django's password reset functionality.

Changing ownership
------------------

.. note::
    This is a to-do item, and an opportunity to contribute to the project!

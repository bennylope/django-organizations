Overview
========

Django group accounts allows you to add multi-user accounts to your application
and tie permissions and actions to organization level accounts.

It uses `django-registration` to handle the account user registration process.

The core of the application consists of these three models:

* Account
* AccountUser
* AccountOwner

The `Account` model represents an organization, the umbrella group by which a
set of users are associated with each other.

The `AccountUser` model is a custom many-to-many class that links a `User`
object to an account.

The `AcountOwner` model is a one-to-one link between an `Account` and an
`AccountUser`.

The group accounts 

Users and multi-account membership
----------------------------------

.. TODO add image showing how these are all related

The key to these relationships is that while an `AccountUser` is associated
with one and only one `Account`, a `User` can be associated with multiple
`AccountUsers` and hence multiple `Accounts`.

.. note::

    This means that the AccountUser class cannot be used as a UserProfile as
    that requires a one-to-one relationship with the User class

In your own project you can associate accounts with things like subscriptions,
documents, and other shared resources, all of which the account users can then
access.

For many projects a simple one-user-per-account model will suffice, and this
can be handled quite ably in your own application's logic.

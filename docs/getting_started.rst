Getting started
===============

django-organizations allows you to add multi-user accounts to your application
and tie permissions and actions to organization level accounts.

The core of the application consists of these three models:

* **Organization** The group object. This is what you would associate your own
  app's functionality with, e.g. subscriptions, repositories, projects, etc.
* **OrganizationUser** A custom `through` model for the ManyToMany relationship
  between the `Organization` model and your user model. It stores additional
  information about the user specific to the organization and provides a
  convenient link for organization ownership.
* **OrganizationOwner** The user with rights over the life and death of the
  organization. This is a one to one relationship with the `OrganizationUser`
  model. This allows users to own multiple organizations and makes it
  easy to enforce ownership from within the organization's membership.

Installation
------------

First add the application to your Python path. The easiest way is to use
`pip`::

    pip install django-organizations

You should install by downloading the source and running::

    $ python setup.py install

Configuration
-------------

First ensure that you have a user system in place to connect to your
organizations. django-organizations will work just fine with the Django's
`contrib.auth` package. To use it, make sure you have `django.contrib.auth`
installed.

Add the `organizations` application to your `INSTALLED_APPS`
list::

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'organizations',
    )

If you plan on using the default URLs, hook the application URLs into your main
application URL configuration in `urls.py`. If you plan on using the
invitation/registration system, set your backend URLs, too::

    from organizations.backends import invitation_backend

    urlpatterns = patterns('',
        ...
        url(r'^accounts/', include('organizations.urls')),
        url(r'^invitations/', include(invitation_backend().get_urls())),
    )

You can specify a different invitation backend in your project settings, and
the `invitation_backend` function will provide the URLs defined by that
backend::

    ORGS_INVITATION_BACKEND = 'myapp.backends.MyInvitationBackend'


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

Views and Mixins
-------------

Hooking the django-organizations URLs into your project provides a default set
of views for accessing and updating organizations and organization membership.

The included `class based views
<https://docs.djangoproject.com/en/1.4/topics/class-based-views/>` are based on
a set of mixins that allow the views to limit access by a user's relationship
to an organization and that query the appropriate organization or user based on
URL keywords.

Implementing in your own project
--------------------------------

While django-organizations has some basic usability 'out-of-the-box', it's
designed to be used as a foundation for project specific functionality. The
view mixins should provide base functionality from which to work for unique
situations.

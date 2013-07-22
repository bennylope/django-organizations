====================
django-organizations
====================

:Info: Groups and multi-user account management
:Version: 0.1.8
:Status: beta
:Author: Ben Lopatin (http://benlopatin.com)

.. image:: https://secure.travis-ci.org/wellfire/django-organizations.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/wellfire/django-organizations

.. image:: https://pypip.in/v/django-organizations/badge.png
    :alt: Current PyPI release
    :target: https://crate.io/packages/django-organizations

.. image:: https://pypip.in/d/django-organizations/badge.png
    :alt: Download count
    :target: https://crate.io/packages/django-organizations

Add user-managed, multi-user groups to your Django project. Use
django-organizations whether your site needs organizations that function like
social groups or multi-user account objects to provide account and subscription
functionality beyond the individual user.

* Relies on `django.contrib.auth` and does not add or require additional user
  or authentication functionality
* Users can be belong to and own more than one organization (account, group)
* Invitation and registration functionality is designed to be flexible to allow
  you to integrate existing invitation and registration apps

Documentation is on `Read the Docs
<http://django-organizations.readthedocs.org/en/latest/index.html>`_

Installing
==========

First add the application to your Python path. The easiest way is to use
`pip`::

    pip install django-organizations

You should install by downloading the source and running::

    $ python setup.py install

Configuring
-----------

Make sure you have `django.contrib.auth` installed, and add the `organizations`
application to your `INSTALLED_APPS` list::

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'organizations',
    )

Then ensure that your project URL conf is updated. You should hook in the
main application URL conf as well as your chosen invitation backend URLs::

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

There is also a lightly tested way to use your own user model, rather than the
default `auth.User` model. Set the `AUTH_USER_MODEL` setting to the dotted
model name of your custom user model, following the procedure in Django 1.5::

    AUTH_USER_MODEL = 'myuserapp.MyUser'

**This is still experimental and your user model's API should hew close to that
of the `auth.User` class.**

Usage Overview
==============

For most use cases it should be sufficient to include the app views directly
using the default URL conf file. You can customize their functionality or
access controls by extending the base views.

There are three models:

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

The underlying organizations API is simple::

    >>> chris = User.objects.get(username="chris")
    >>> soundgarden = create_organization(chris, "Soundgarden")
    >>> soundgarden.is_user(chris)
    True
    >>> soundgarden.is_admin(chris)
    True
    >>> soundgarden.owner.organization_user
    <OrganizationUser: Chris Cornell>
    >>> soundgarden.owner.organization_user.user
    >>> <User: chris>
    >>> audioslave = create_organization(chris, "Audioslave")
    >>> tom = User.objects.get(username="tom")
    >>> audioslave.add_user(tom, is_admin=True)
    <OrganizationUser: Tom Morello>


Overview
--------

Each organization can have only one owner, however a site user can be a member
of multiple organizations, or own multiple organizations. The OrganizationUser
model servers as an intermediary between the `Organization` and the `Users` to
allow this.

Development & Contributing
==========================

Development is on-going. To-do items have been moved to the wiki for the time
being.

The basic functionality should not need much extending. Current dev priorities
for me and contributors should include:

* Improving the tests and test coverage (ideally moving them back out of the
  main module and executable using the setup.py file)
* Improving the backends and backends concept so that additional invitation and
  registration backends can be used
* Documentation
* Ensuring all application text is translatable
* Python 3 readiness
* Configurable user model (a la Django 1.5's anticipated auth.User rewrite)

Please use the project's issues tracker to report bugs, doc updates, or other
requests/suggestions.

Targets
-------

The codebase is targeted at tested against:

* Django 1.4.x against Python 2.6 and Python 2.7
* Django 1.5.x against Python 2.6, Python 2.7, and Python 3.3
* Django 1.6.x (beta) against Python 2.7 and Python 3.3

Submitting
----------

These submission guidelines will make it more likely your submissions will be
reviewed and make it into the project:

* Ensure they match the project goals and are sufficiently generalized
* Please try to follow `Django coding style
  <https://docs.djangoproject.com/en/1.4/internals/contributing/writing-code/coding-style/>`_.
  The code base style isn't all up to par, but I'd like it to move in that
  direction
* Also please try to include `good commit log messages
  <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
* Pull requests should include a quantity amount of code and commits that are
  reasonable to review, are logically grouped, and based off clean feature
  branches.

Code contributions are expected to pass in all three target environments, and
pull requests should be made from branches with passing builds.

Project goals
-------------

django-organizations should be backend agnostic:

1. Authentication agnostic
2. Registration agnostic
3. Invitation agnostic
4. User messaging agnostic

Etc.

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.

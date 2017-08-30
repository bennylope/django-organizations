====================
django-organizations
====================

.. start-table

.. list-table::
    :stub-columns: 1

    * - Summary
      - Groups and multi-user account management
    * - Author
      - Ben Lopatin (http://benlopatin.com / https://wellfire.co)
    * - Status
      - |docs| |travis| |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/django-organizations/badge/?style=flat
    :target: https://readthedocs.org/projects/django-organizations
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/bennylope/django-organizations.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bennylope/django-organizations

.. |version| image:: https://img.shields.io/pypi/v/django-organizations.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/django-organizations

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-organizations.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/django-organizations

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/django-organizations.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/django-organizations

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/django-organizations.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/django-organizations


.. end-table


Separate individual user identity from accounts and subscriptions. Django
Organizations adds user-managed, multi-user groups to your Django project. Use
Django Organizations whether your site needs organizations that function like
social groups or multi-user account objects to provide account and subscription
functionality beyond the individual user.

* Works with your existing user model, whether
  `django.contrib.auth` or a custom model. No additional user
  or authentication functionality required.
* Users can be belong to and own more than one organization (account, group)
* Invitation and registration functionality works out of the box for many
  situations and can be extended as need to fit specific requirements.
* Start with the base models or use your own for greater customization.

Documentation is on `Read the Docs
<http://django-organizations.readthedocs.org/en/latest/index.html>`_

Installing
==========

First add the application to your Python path. The easiest way is to use
`pip`::

    pip install django-organizations

You can also install by downloading the source and running::

    $ python setup.py install

By default you will need to install `django-extensions` or comparable libraries
if you plan on adding Django Organizations as an installed app to your Django
project. See below on configuring.

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

    urlpatterns = [
        ...
        url(r'^accounts/', include('organizations.urls')),
        url(r'^invitations/', include(invitation_backend().get_urls())),
    ]

Auto slug field
~~~~~~~~~~~~~~~

The standard way of using Django Organizations is to use it as an installed app
in your Django project. Django Organizations will need to use an auto slug
field which are not included. By default it will try to import these from
django-extensions, but you can configure your own in settings. The default::

    ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'

Alternative::

    ORGS_SLUGFIELD = 'autoslug.fields.AutoSlugField'

Previous versions allowed you to specify an `ORGS_TIMESTAMPED_MODEL` path. This
is now ignored and the functionality satisifed by a vendored solution. A
warning will be given but this *should not* have any effect on your code.

- `django-extensions <http://django-extensions.readthedocs.org/en/latest/>`_
- `Django Autoslug <https://pythonhosted.org/django-autoslug/>`_

Registration & invitation backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify a different invitation backend in your project settings, and
the `invitation_backend` function will provide the URLs defined by that
backend::

    INVITATION_BACKEND = 'myapp.backends.MyInvitationBackend'


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

    >>> from organizations.utils import create_organization
    >>> chris = User.objects.get(username="chris")
    >>> soundgarden = create_organization(chris, "Soundgarden", org_user_defaults={'is_admin': True})
    >>> soundgarden.is_member(chris)
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

Custom models
-------------

Django-organizations can act as a base library (not installed in your project)
and used to create unique organization model sets using custom tables. See the
`Cooking with Django Organizations
<http://django-organizations.readthedocs.org/en/latest/cookbook.html#advanced-customization>`_
section in the documentation for advice on proceeding.

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

Please use the project's issues tracker to report bugs, doc updates, or other
requests/suggestions.

Targets & testing
-----------------

The codebase is targeted and tested against:

* Django 1.8.x against Python 2.7, 3.4, 3.5, and PyPy
* Django 1.9.x against Python 2.7, 3.4, 3.5, and PyPy
* Django 1.10.x against Python 2.7, 3.4, 3.5, 3.6, and PyPy
* Django 1.11.x against Python 2.7, 3.4, 3.5, 3.6, and PyPy

To run the tests against all target environments, install `tox
<https://testrun.org/tox/latest/>`_ and then execute the command::

    tox

Fast testing
------------

Testing each change on all the environments takes some time, you may
want to test faster and avoid slowing down development by using pytest
against your current environment::

    pip install -r requirements-test.txt
    py.test

Supply the ``-x`` option for **failfast** mode::

    py.test -x

Submitting
----------

These submission guidelines will make it more likely your submissions will be
reviewed and make it into the project:

* Ensure they match the project goals and are sufficiently generalized
* Please try to follow `Django coding style
  <https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/>`_.
  The code base style isn't all up to par, but I'd like it to move in that
  direction
* Also please try to include `good commit log messages
  <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
* Pull requests should include an amount of code and commits that are
  reasonable to review, are **logically grouped**, and based off clean feature
  branches.

Code contributions are expected to pass in all target environments, and
pull requests should be made from branches with passing builds on `Travis
CI <https://travis-ci.org/bennylope/django-organizations>`_.

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

Anyone is free to use or modify this software under the terms of the BSD
license.

.. :changelog:

History
=======

2.2.0
-----

* Remove support for Django < 3.2
* Remove support for Python 3.7
* Fix trove classifiers

2.1.0
-----

* Adds migrations to support Django 4.x
* Removes support for Django < 3.2
* Updates tox testing for supported configurations of Django 3.2 - 4.1 with Python 3.7 - 3.10
* Early tox testing of Django 4.1 with Python 3.11
* Fixes GitHub Actions automated testing

2.0.2
-----

* Remove `default_app_config` for forward compatiblity with Django 4.1

2.0.1
-----

* Better compatibility with Django 3.2

2.0.0
-----

* Invitation model backend uses models to track invitations
* Registration/inviation backends take an optional namespace argument on initialization. The use
  case is if you want to namespace the URLs
* Can provide a dotted path to `invitation_backend` and `registration_backend` functions
* Drops support for Python 2 and Django versions < 2.2 LTS
* Migrate the codebase to an src/ layout
* Now with more test coverage!


1.1.1
-----

* Fixes issue with default backend where users defined without first/last names
  might not be represented

1.1.0
-----

* Migrations and slug related fixup

This is a small but significant change. A change introduced in version 1.0.0 due to
incompatability with an unmaintained default dependency yielded migration issues for
many users. This release switches *back* to a *fork* of the original dependency
to revert the default changes.

1.0.0
-----

* Django 2 compatibility.

At this point it seems reasonable to bump to version 1.

0.9.3
-----

* Create username value for user if username field exists (custom user models)
* Replaced BaseBackend._send_email with BaseBackend.email_message. email_message() should return
  the message without actually doing the send.

0.9.2
-----

* Decouple concrete organizations.Organization model from the invitation/registration backends

0.9.1
-----

* Fixes missing migration. Migration was created due to non-schema changes in models

0.9.0
-----

* Add notification to users when added to an organization
* New abstract models create separation between 'plain' base models and abstract
  models that include abstracted functionality previously included only in
  concrete models
* Python 3.6 and Django 1.11 test support

0.8.2
-----

* Updates setup classifiers information

0.8.1
-----

* Fixes [lack of] validation bug in backend registration form

0.8.0
-----

* Adds Django 1.10 support

0.7.0
-----

Fixes some issues which may require some users to clear out extraneous
migrations produced by using configurable base classes.

* Fixes condition where `create_organization` produces an owner who is not an
  admin user.
* Fixes issue in slug field import resulting in spurious migrations.
* Immediately deprecates configurable TimeStampedModel import. This caused
  serious problems with Django's migration library which were not easily
  resolved for a feature that added little value.

0.6.1
-----

* Fixes email parsing from settings

0.6.0
-----

* Adds Django 1.9 support
* Drops support for Django 1.7
* Fixes migration issue related to incomplete support for configurable model
  fields and base model. If you are upgrading (especially from a fork of the
  development version of django-organization) you may have an extra migration,
  0002_auto_20151005_1823, which has been removed.

0.5.3
-----

* Fixes migrations problem in build

0.5.2
-----

* Fixes packaging bug

0.5.1
-----

* Cleaned up installation instructions

0.5.0
-----

* Drops testing support for Django 1.5 and Django 1.6
* Adds native Django database migrations
* Adds tested support for Django 1.7 and Django 1.8

0.4.3
-----

* Adds app specific signals

0.4.2
-----

* Various related name fixes in models, registration backends

0.4.1
-----

* Support for older Django versions with outdated versions of `six`

0.4.0
-----

* Allows for configurable TimeStampModel (base mixin for default Organization
  model) and AutoSlugField (field on default Organization model).

0.3.0
-----

* Initial Django 1.7 compatability release

0.2.3
-----

* Fix issue validating organziation ownership for custom organization models
  inheriting directly from the `Organization` class.

0.2.2
-----

* Packaging fix

0.2.1
-----

* Packaging fix

0.2.0
-----

* Abstract base models. These allow for custom organization models
  without relying on mulit-table inheritence, as well as custom
  organization user models, all on an app-by-app basis.

0.1.10
------

* Packaging fix

0.1.9
-----

* Restructures tests to remove from installed module, should reduce installed
  package size

0.1.8
-----

* Fixes *another* bug in email invitations

0.1.7
-----

* Fixes bug in email invitation

0.1.6
-----

* Extends organizaton name length
* Increase email field max length
* Adds `get_or_add_user` method to Organization
* Email character escaping

0.1.5
-----

* Use raw ID fields in admin
* Fixes template variable names
* Allow superusers access to all organization views
* Activate related organizations when activating an owner user

0.1.4a
------

* Bug fix for user model import

0.1.4
-----

* Bugfixes for deleting organization users
* Removes additional `auth.User` references in app code

0.1.3b
------

* Changes SlugField to an AutoSlugField from django-extensions
* Base models on TimeStampedModel from django-extensions
* ForeignKey to user model based on configurable user selection

0.1.3
-----

* Manage organization models with South
* Added configurable context variable names to view mixins
* Added a base backend class which the Invitation and Registration backends extend
* Lengthed Organization name and slug fields
* Makes mixin model classes configurable
* Improved admin display
* Removes initial passwords

0.1.2
-----

* Added registration backend
* Various bug fixes

0.1.1
-----

* Add RequestContext to default invitation registration view
* Fix invitations

0.1.0
-----

* Initial alpha application

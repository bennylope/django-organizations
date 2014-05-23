.. :changelog:

History
=======

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

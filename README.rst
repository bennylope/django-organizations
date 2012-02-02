=====================
Django group accounts
=====================

Create and manage group accounts in Django projects and allow users to be
members of multiple accounts.

Project status
==============

Let's get this out of the way right now. This is definitely pre-alpha! This is
hardly feature complete, and it's still exploratory.

Use case
========

It's an incredibly requirement to have not just users on your web site or
application but users who are members of a larger group account. This might be
an additional feature, or it might be a core feature (GitHub has optional group
accounts, Basecamp has required group accounts). Any place where the account is
or can be based on a group of people, rather than just one individual.

Installing
==========

First add the application to your Python path. The easiest way is to use `pip`:

    pip install django-group-accounts

Then make sure that you add the `accounts` application to your
`INSTALLED_APPS` list.

Using group accounts
====================

Overview
--------

The group accounts application relies on Django's auth app for the User model.
It offers no authentication of its own. There are three models:

* Account
* AccountUser
* AccountOwner

Each account can have only one owner however a site user can be a member of
multiple organizations. The AccountUser model servers as an intermediary
between the Account and the Users to allow this.

Ideally as much of the relationships should be defined in the database.

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.

To-do
=====

* Merge users if someone has duplicate user profiles (or just validate that a
  user can have only one AccountUser object per Account)


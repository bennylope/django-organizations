# -*- coding: utf-8 -*-

import django.dispatch

user_added = django.dispatch.Signal()
user_removed = django.dispatch.Signal()
invitation_accepted = django.dispatch.Signal()
owner_changed = django.dispatch.Signal()

import django.dispatch

user_kwargs = {"providing_args": ["user"]}
user_added = django.dispatch.Signal(**user_kwargs)
user_removed = django.dispatch.Signal(**user_kwargs)

owner_kwargs = {"providing_args": ["old", "new"]}
owner_changed = django.dispatch.Signal(**owner_kwargs)

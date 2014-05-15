from .models import Organization


def create_organization(user, name,
        org_defaults={}, org_user_defaults={}, **kwargs):
    """
    Returns a new organization, also creating an initial organization user who
    is the owner.

    The specific models can be specified if a custom organization app is used.
    The simplest way would be to use a partial.

    >>> from organizations.utils import create_organization
    >>> from myapp.models import Account
    >>> from functools import partial
    >>> create_account = partial(create_organization, model=Account)

    """
    # TODO try to add in backwards compatability
    org_model = kwargs.pop('model', None) or kwargs.pop('org_model', None) or Organization
    kwargs.pop('org_user_model', None)  # Discard deprecated argument
    org_user_klass = org_model.organization_users.related.model
    org_owner_klass = org_model.owner.related.model

    #if slug is not None:
    #    org_defaults.update({'slug': slug})
    #if is_active is not None:
    #    org_defaults.update({'is_active': is_active})
    #if is_admin is not None:
    #    org_user_defaults.update({'is_admin': is_admin})

    organization = org_model.objects.create(name=name, **org_defaults)
    new_user = org_user_klass.objects.create(organization=organization,
            user=user, **org_user_defaults)
    org_owner_klass.objects.create(organization=organization,
            organization_user=new_user)
    return organization


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)

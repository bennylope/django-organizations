from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)


def create_organization(user, name, slug, is_active=True,
        org_model=Organization, org_user_model=OrganizationUser):
    """
    Returns a new organization, also creating an initial organization user who
    is the owner.

    The specific models can be specified if a custom organization app is used.
    The simplest way would be to use a partial.

    >>> from organizations.utils import create_organization
    >>> from myapp.models import Account, AccountUser
    >>> from functools import partial
    >>> create_account = partial(create_organization,
                org_model=Account, org_user_model=AccountUser)

    """
    organization = org_model.objects.create(name=name, slug=slug,
            is_active=is_active)
    new_user = org_user_model.objects.create(organization=organization,
            user=user, is_admin=True)
    OrganizationOwner.objects.create(organization=organization,
            organization_user=new_user)
    return organization


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)

from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)

# TODO: manager method? override `create` or add this one
def create_organization(name, owner):
    """
    Returns a new organization, also creating an initial organization user who
    is the owner.
    """
    organization = Organization.objects.create(name=name)
    new_user = OrganizationUser.objects.create(organization=organization,
            user=owner, is_admin=True)
    OrganizationOwner.objects.create(organization=organization,
            organization_user=new_user)
    return organization


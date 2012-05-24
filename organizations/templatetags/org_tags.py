from django import template

register = template.Library()


@register.inclusion_tag('organizations/organization_users.html')
def organization_users(org):
    return {'organization_users': org.organization_users.all()}

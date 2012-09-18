from django import template

register = template.Library()


@register.inclusion_tag('organizations/organization_users.html', takes_context=True)
def organization_users(context, org):
    context.update({'organization_users': org.organization_users.all()})
    return context

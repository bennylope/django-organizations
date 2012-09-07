from django import template

register = template.Library()

@register.filter
def is_admin(org,user):
    return org.is_admin(user)
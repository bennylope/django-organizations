from django import template

register = template.Library()

@register.filter
def is_admin(org, user):
    return org.is_admin(user)

@register.filter
def is_member(org, user):
    return org.is_member(user)

@register.filter
def is_owner(org, user):
    return org.is_owner(user)
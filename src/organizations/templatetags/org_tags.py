# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag("organizations/organization_users.html", takes_context=True)
def organization_users(context, org):
    context.update({"organization_users": org.organization_users.all()})
    return context


@register.filter
def is_admin(org, user):
    return org.is_admin(user)


@register.filter
def is_owner(org, user):
    return org.owner.organization_user.user == user

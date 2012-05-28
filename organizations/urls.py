from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from organizations.views import (OrganizationList, OrganizationDetail,
        OrganizationUpdate, OrganizationDelete, OrganizationCreate,
        OrganizationUserList, OrganizationUserDetail, OrganizationUserUpdate,
        OrganizationUserCreate, OrganizationUserRemind, OrganizationUserDelete)


urlpatterns = patterns('',
    # Organization URLs
    url(r'^$', view=login_required(OrganizationList.as_view()),
        name="organization_list"),
    url(r'^add/$', view=login_required(OrganizationCreate.as_view()),
        name="organization_add"),
    url(r'^(?P<organization_pk>[\d]+)/$',
        view=login_required(OrganizationDetail.as_view()),
        name="organization_detail"),
    url(r'^(?P<organization_pk>[\d]+)/edit/$',
        view=login_required(OrganizationUpdate.as_view()),
        name="organization_edit"),
    url(r'^(?P<organization_pk>[\d]+)/delete/$',
        view=login_required(OrganizationDelete.as_view()),
        name="organization_delete"),

    # Organization user URLs
    url(r'^(?P<organization_pk>[\d]+)/people/$',
        view=login_required(OrganizationUserList.as_view()),
        name="organization_user_list"),
    url(r'^(?P<organization_pk>[\d]+)/people/add/$',
        view=login_required(OrganizationUserCreate.as_view()),
        name="organization_user_add"),
    url(r'^(?P<organization_pk>[\d]+)/people/(?P<user_pk>[\d]+)/remind/$',
        view=login_required(OrganizationUserRemind.as_view()),
        name="organization_user_remind"),
    url(r'^(?P<organization_pk>[\d]+)/people/(?P<user_pk>[\d]+)/$',
        view=login_required(OrganizationUserDetail.as_view()),
        name="organization_user_detail"),
    url(r'^(?P<organization_pk>[\d]+)/people/(?P<user_pk>[\d]+)/edit/$',
        view=login_required(OrganizationUserUpdate.as_view()),
        name="organization_user_edit"),
    url(r'^(?P<organization_pk>[\d]+)/people/(?P<user_pk>[\d]+)/delete/$',
        view=login_required(OrganizationUserDelete.as_view()),
        name="organization_user_delete"),
)

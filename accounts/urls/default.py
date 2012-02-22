from django.conf.urls.defaults import patterns, url

from accounts.views import (AccountList, AccountDetail, AccountUpdate,
        AccountDelete, AccountCreate, AccountUserList, AccountUserDetail,
        AccountUserUpdate, AccountUserCreate, AccountUserDelete)


urlpatterns = patterns('',
    # Account URLs
    url(r'^$', view=AccountList.as_view(), name="account_list"),
    url(r'^add/$', view=AccountCreate.as_view(), name="account_add"),
    url(r'^(?P<account_pk>[\d]+)/$', view=AccountDetail.as_view(),
        name="account_detail"),
    url(r'^(?P<account_pk>[\d]+)/edit/$', view=AccountUpdate.as_view(),
        name="account_edit"),
    url(r'^(?P<account_pk>[\d]+)/delete/$', view=AccountDelete.as_view(),
        name="account_delete"),

    # Account user URLs
    url(r'^(?P<account_pk>[\d]+)/people/$', view=AccountUserList.as_view(),
        name="accountuser_list"),
    url(r'^(?P<account_pk>[\d]+)/people/add/$',
        view=AccountUserCreate.as_view(), name="accountuser_add"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/$',
        view=AccountUserDetail.as_view(), name="accountuser_detail"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/edit/$',
        view=AccountUserUpdate.as_view(), name="accountuser_edit"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/delete/$',
        view=AccountUserDelete.as_view(), name="accountuser_delete"),
)

from django.conf.urls.defaults import patterns, url

from accounts.views.base import (BaseAccountList, BaseAccountDetail,
        BaseAccountUpdate, BaseAccountDelete, BaseAccountCreate,
        BaseAccountUserList, BaseAccountUserDetail, BaseAccountUserUpdate,
        BaseAccountUserCreate, BaseAccountUserDelete)


urlpatterns = patterns('',
    # BaseAccount URLs
    url(r'^$', view=BaseAccountList.as_view(), name="base_account_list"),
    url(r'^add/$', view=BaseAccountCreate.as_view(), name="base_account_add"),
    url(r'^(?P<account_pk>[\d]+)/$', view=BaseAccountDetail.as_view(),
        name="base_account_detail"),
    url(r'^(?P<account_pk>[\d]+)/edit/$', view=BaseAccountUpdate.as_view(),
        name="base_account_edit"),
    url(r'^(?P<account_pk>[\d]+)/delete/$', view=BaseAccountDelete.as_view(),
        name="base_account_delete"),

    # BaseAccount user URLs
    url(r'^(?P<account_pk>[\d]+)/people/$', view=BaseAccountUserList.as_view(),
        name="base_accountuser_list"),
    url(r'^(?P<account_pk>[\d]+)/people/add/$',
        view=BaseAccountUserCreate.as_view(), name="base_accountuser_add"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/$',
        view=BaseAccountUserDetail.as_view(), name="base_accountuser_detail"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/edit/$',
        view=BaseAccountUserUpdate.as_view(), name="base_accountuser_edit"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/delete/$',
        view=BaseAccountUserDelete.as_view(), name="base_accountuser_delete"),
)







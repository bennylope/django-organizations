from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from accounts.views import (AccountList, AccountDetail, AccountUpdate,
        AccountDelete, AccountCreate, AccountUserList, AccountUserDetail,
        AccountUserUpdate, AccountUserCreate, AccountUserDelete,
        UserProfileView)


urlpatterns = patterns('',
    # Account URLs
    url(r'^$', view=login_required(AccountList.as_view()),
        name="account_list"),
    url(r'^add/$', view=login_required(AccountCreate.as_view()),
        name="account_add"),
    url(r'^(?P<account_pk>[\d]+)/$',
        view=login_required(AccountDetail.as_view()),
        name="account_detail"),
    url(r'^(?P<account_pk>[\d]+)/edit/$',
        view=login_required(AccountUpdate.as_view()),
        name="account_edit"),
    url(r'^(?P<account_pk>[\d]+)/delete/$',
        view=login_required(AccountDelete.as_view()),
        name="account_delete"),

    # Account user URLs
    url(r'^(?P<account_pk>[\d]+)/people/$',
        view=login_required(AccountUserList.as_view()),
        name="account_user_list"),
    url(r'^(?P<account_pk>[\d]+)/people/add/$',
        view=login_required(AccountUserCreate.as_view()),
        name="account_user_add"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<account_user_pk>[\d]+)/$',
        view=login_required(AccountUserDetail.as_view()),
        name="account_user_detail"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<account_user_pk>[\d]+)/edit/$',
        view=login_required(AccountUserUpdate.as_view()),
        name="account_user_edit"),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<account_user_pk>[\d]+)/delete/$',
        view=login_required(AccountUserDelete.as_view()),
        name="account_user_delete"),

    # Profile
    # This view should be configurable for a custom UserProfile class
    url(r'^profile/$', view=login_required(UserProfileView.as_view()),
        name="account_user_profile"),
)


from django.conf.urls.defaults import patterns, url

from accounts.views import (AccountList, AccountDetail, AccountUpdate,
        AccountDelete, AccountCreate, AccountUserList, AccountUserDetail,
        AccountUserUpdate, AccountUserCreate, AccountUserDelete, LoginView,
        LogoutView, UserProfileView)


urlpatterns = patterns('',
    # Authentication
    url(r'^login/$', view=LoginView.as_view(), name='login'),
    url(r'^logout/$', view=LogoutView.as_view(), name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        name='password_reset'),
    url(r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),

    #Registration
    #url(r'^register/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    view=UserRegistration.as_view(), name='user_registration'),

    # Account URLs
    url(r'^$', view=AccountList.as_view(), name='account_list'),
    url(r'^add/$', view=AccountCreate.as_view(), name='account_add'),
    url(r'^(?P<account_pk>[\d]+)/$', view=AccountDetail.as_view(),
        name='account_detail'),
    url(r'^(?P<account_pk>[\d]+)/edit/$', view=AccountUpdate.as_view(),
        name='account_edit'),
    url(r'^(?P<account_pk>[\d]+)/delete/$', view=AccountDelete.as_view(),
        name='account_delete'),

    # Account user URLs
    url(r'^(?P<account_pk>[\d]+)/people/$', view=AccountUserList.as_view(),
        name='accountuser_list'),
    url(r'^(?P<account_pk>[\d]+)/people/add/$',
        view=AccountUserCreate.as_view(), name='accountuser_add'),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/$',
        view=AccountUserDetail.as_view(), name='accountuser_detail'),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/edit/$',
        view=AccountUserUpdate.as_view(), name='accountuser_edit'),
    url(r'^(?P<account_pk>[\d]+)/people/(?P<accountuser_pk>[\d]+)/delete/$',
        view=AccountUserDelete.as_view(), name='accountuser_delete'),

    # Profile
    url(r'^profile/$', view=UserProfileView.as_view(),
        name="accountuser_profile"),
)

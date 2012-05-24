from django.conf.urls.defaults import patterns, url, include

from organizations.invitations.views import RegisterInvite


urlpatterns = patterns('',
    url(r'^(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=RegisterInvite.as_view(), name="invitations_register"),
)



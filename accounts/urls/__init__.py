from django.conf.urls.defaults import patterns, url, include



urlpatterns = patterns('',
    url(r'', include('accounts.urls.base')),
)

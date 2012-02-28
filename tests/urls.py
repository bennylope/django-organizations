from django.conf.urls.defaults import url, patterns, include

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts_base/', include('accounts.urls.base')),
)


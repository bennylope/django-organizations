from django.conf.urls import patterns, include, url
from django.contrib import admin

from organizations.backends import invitation_backend

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^invite/', include(invitation_backend().get_urls())),
)

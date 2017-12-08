from django.conf.urls import include, url
from django.contrib import admin

from organizations.backends import invitation_backend, registration_backend

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^invite/', include(invitation_backend().get_urls())),
    url(r'^register/', include(registration_backend().get_urls())),
]

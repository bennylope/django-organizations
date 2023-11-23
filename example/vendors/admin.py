from django.contrib import admin

from .models import Vendor
from .models import VendorOwner
from .models import VendorUser

admin.site.register(Vendor)
admin.site.register(VendorUser)
admin.site.register(VendorOwner)

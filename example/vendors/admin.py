from django.contrib import admin

from .models import Vendor, VendorUser, VendorOwner


admin.site.register(Vendor)
admin.site.register(VendorUser)
admin.site.register(VendorOwner)

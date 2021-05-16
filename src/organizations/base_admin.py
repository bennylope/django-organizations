# -*- coding: utf-8 -*-

from django.contrib import admin


class BaseOwnerInline(admin.StackedInline):
    raw_id_fields = ("organization_user",)


class BaseOrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_filter = ("is_active",)


class BaseOrganizationUserAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "is_admin"]
    raw_id_fields = ("user", "organization")


class BaseOrganizationOwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ("organization_user", "organization")

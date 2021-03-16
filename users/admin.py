from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Software, Package

admin.site.unregister(User)
admin.site.unregister(Group)
# admin.site.unregister(Site)

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'type', 'expiry')
    list_filter = ('user', 'name')
    search_fields = ('user', 'name')

    def has_add_permission(self, request, obj=None):
        return False

class PackageAdmin(admin.ModelAdmin):
    readonly_fields = ('dt', 'updated')


# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_active',)
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     def get_queryset(self, request):
#         qs = super(CustomUserAdmin, self).get_queryset(request)
#         return qs.filter(is_superuser=False)

admin.site.register(Software, SoftwareAdmin)
admin.site.register(Package, PackageAdmin)
from django.contrib.gis import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class RegionAdmin(admin.GeoModelAdmin):
    search_fields = ['name', 'uuid']
    list_display = ['uuid', 'name']


class VendorInline(admin.StackedInline):
    model = models.Vendor
    can_delete = False
    verbose_name_plural = 'vendors'


class UserAdmin(BaseUserAdmin):
    # Edit user and vendor info together
    inlines = (VendorInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Region, RegionAdmin)

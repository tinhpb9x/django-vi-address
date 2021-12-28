from django.contrib import admin
from .models import City, District, Ward


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'slug', 'type', 'name_with_type']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'slug', 'type', 'name_with_type', 'path', 'path_with_type', 'parent_code']


class WardAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'slug', 'type', 'name_with_type', 'path', 'path_with_type', 'parent_code']


admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Ward, WardAdmin)

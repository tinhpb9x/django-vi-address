from django.contrib import admin
from .models import City, Ward


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'slug', 'type', 'name_with_type']


class WardAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'slug', 'type', 'name_with_type', 'path', 'path_with_type', 'parent_code']


admin.site.register(City, CityAdmin)
admin.site.register(Ward, WardAdmin)

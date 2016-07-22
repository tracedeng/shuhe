from django.contrib import admin

# Register your models here.
from region.models import Province, City, County


class ProvinceAdmin(admin):
    list_display = ('name', 'e_name')


class CityAdmin(admin):
    list_display = ('name', 'e_name', 'province')


class CountyAdmin(admin):
    list_display = ('name', 'e_name', 'city')


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(County, CountyAdmin)
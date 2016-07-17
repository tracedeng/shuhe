from django.contrib import admin

# Register your models here.
from market.models import Appliances, Agent, Maintenance, Order


class AppliancesAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'wechat')
    search_fields = ('name',)


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


admin.site.register(Appliances, AppliancesAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Maintenance)
admin.site.register(Order)
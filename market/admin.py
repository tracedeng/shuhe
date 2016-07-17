from django.contrib import admin

# Register your models here.
from market.models import Softener, Purifier,Drinking, Agent, Maintenance, Order


class SoftenerAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size', 'service_flow', 'salt_tank_capacity', 'resin_quantity', 'resin_tank_size', 'regeneration_time', 'maximum_water_hardness', 'maximum_grains', 'maximum_iron_treatment')

class PurifierAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size', 'filtering_accuracy', 'rated_flow', 'maximum_flow', 'water_pressure', 'water_temperature', 'cartridge_life')


class DrinkingAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size', 'maximum_tds', 'maximum_flow', 'water_pressure', 'water_temperature', 'activated_carbon', 'ro_film')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'wechat')
    search_fields = ('name',)


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


admin.site.register(Softener, SoftenerAdmin)
admin.site.register(Purifier, PurifierAdmin)
admin.site.register(Drinking, DrinkingAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Maintenance)
admin.site.register(Order)

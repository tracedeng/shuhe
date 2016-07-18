from django.contrib import admin

# Register your models here.
from market.models import Softener, Purifier,Drinking, Agent, Maintenance, Order, Equipment, HeatSpec, AirSpec, \
    SoundOffSpec, StrongSpec, CircularSpec, HiddenSpec, VentilationSpec, EquipmentCategories


class SoftenerAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size', 'service_flow',
                    'salt_tank_capacity', 'resin_quantity', 'resin_tank_size', 'regeneration_time',
                    'maximum_water_hardness', 'maximum_grains', 'maximum_iron_treatment')

class PurifierAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size',
                    'filtering_accuracy', 'rated_flow', 'maximum_flow', 'water_pressure', 'water_temperature',
                    'cartridge_life')


class DrinkingAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'price', 'outline_dimension', 'interface_size', 'maximum_tds',
                    'maximum_flow', 'water_pressure', 'water_temperature', 'activated_carbon', 'ro_film')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('identification', 'description', 'name')


class EquipmentCategoriesAdmin(admin.ModelAdmin):
    list_display = ('categories', 'img_name', 'group')


class VentilationSpecAdmin(admin.ModelAdmin):
    list_display = ('operation_mode', 'secondary_mode', 'power_consumption', 'ventilation_volume', 'air_volume',
                    'noise', 'maximum_pressure', 'host_weight', 'pipeline', 'size')
    filter_horizontal = ("equipment",)


class HeatSpecAdmin(admin.ModelAdmin):
    list_display = ('air_volume', 'power_consumption', 'noise', 'recovery_rate', 'applicable_area', 'host_size',
                    'maximum_pressure', 'net_weight', 'pipeline')
    filter_horizontal = ("equipment",)


class AirSpecAdmin(admin.ModelAdmin):
    list_display = ('host_size', 'hoisting_size', 'air_volume', 'weight', 'pipeline')
    filter_horizontal = ("equipment",)


class SoundOffSpecAdmin(admin.ModelAdmin):
    list_display = ('voltage', 'power_consumption', 'ventilation_volume', 'noise', 'maximum_pressure', 'opening_size',
                    'host_weight', 'pipeline')
    filter_horizontal = ("equipment",)


class StrongSpecAdmin(admin.ModelAdmin):
    list_display = ('voltage', 'power_consumption', 'ventilation_volume', 'noise', 'maximum_pressure', 'opening_size',
                    'host_weight', 'pipeline')
    filter_horizontal = ("equipment",)


class CircularSpecAdmin(admin.ModelAdmin):
    list_display = ('power_consumption', 'air_volume', 'noise', 'installation_dimensions', 'applicable_area', 'weight')
    filter_horizontal = ("equipment",)

class HiddenSpecAdmin(admin.ModelAdmin):
    list_display = ('voltage', 'power_consumption', 'ventilation_volume', 'noise', 'maximum_pressure', 'host_size',
                    'host_weight', 'pipeline')
    filter_horizontal = ("equipment",)


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'wechat')


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


# GE
admin.site.register(Softener, SoftenerAdmin)
admin.site.register(Purifier, PurifierAdmin)
admin.site.register(Drinking, DrinkingAdmin)

# LifeGear
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentCategories, EquipmentCategoriesAdmin)
admin.site.register(VentilationSpec, VentilationSpecAdmin)
admin.site.register(HeatSpec, HeatSpecAdmin)
admin.site.register(AirSpec, AirSpecAdmin)
admin.site.register(SoundOffSpec, SoundOffSpecAdmin)
admin.site.register(StrongSpec, StrongSpecAdmin)
admin.site.register(CircularSpec, CircularSpecAdmin)
admin.site.register(HiddenSpec, HiddenSpecAdmin)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Maintenance)
admin.site.register(Order)

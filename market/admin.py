from django.contrib import admin

# Register your models here.
from market.models import Appliances, Agent, Maintenance, Order


admin.site.register(Appliances)
admin.site.register(Agent)
admin.site.register(Maintenance)
admin.site.register(Order)
from django.contrib import admin

from foodwagon_backend.models import Venues,Trucks,Chef,Ordered_Chef
from .models import *

admin.site.register(Venues)
admin.site.register(Trucks)
admin.site.register(Chef)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItemTruck)
admin.site.register(OrderItemVenue)
admin.site.register(OrderItemChef)
admin.site.register(Order)
admin.site.register(Ordered_Chef)


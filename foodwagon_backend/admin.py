from django.contrib import admin

from foodwagon_backend.models import Venues,Trucks,Chef,Ordered_Chef,Ordered_Venue
from .models import Venues,Trucks,Chef,Ordered_Chef,Ordered_Venue

admin.site.register(Venues)
admin.site.register(Trucks)
admin.site.register(Chef)
admin.site.register(Ordered_Chef)
admin.site.register(Ordered_Venue)


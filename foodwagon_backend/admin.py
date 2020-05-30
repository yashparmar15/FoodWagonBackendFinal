from django.contrib import admin

from foodwagon_backend.models import Venues,Trucks,Chef
from .models import Venues,Trucks,Chef

admin.site.register(Venues)
admin.site.register(Trucks)
admin.site.register(Chef)


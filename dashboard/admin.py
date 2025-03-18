from django.contrib import admin
from .models import WaterWell

class WaterWellAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at', 'updated_at')
    filter_horizontal = ('users',)

admin.site.register(WaterWell, WaterWellAdmin)
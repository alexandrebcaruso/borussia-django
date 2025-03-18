from django.contrib import admin
from .models import WaterWellUsage

class WaterWellUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'water_well', 'date', 'water_usage', 'location')
    search_fields = ('water_well__name', 'location')
    list_filter = ('date',)
    filter_horizontal = ()

admin.site.register(WaterWellUsage, WaterWellUsageAdmin)
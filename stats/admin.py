from django.contrib import admin
from stats.models import WaterWell, WaterWellUsage

class WaterWellUserInline(admin.TabularInline):
    model = WaterWell.users.through
    extra = 0

@admin.register(WaterWell)
class WaterWellAdmin(admin.ModelAdmin):
    inlines = [WaterWellUserInline]
    list_display = (
        'public_id', 
        'name', 
        'uf', 
        'locality',
        'latitude',
        'longitude',
        'original_crs'
    )
    search_fields = ('public_id', 'name', 'locality')
    list_filter = ('uf', 'nature', 'original_crs')
    readonly_fields = ('original_crs',)
    fieldsets = (
        (None, {
            'fields': ('public_id', 'name', 'uf', 'locality', 'nature')
        }),
        ('Coordenadas', {
            'fields': (
                ('latitude', 'longitude'),
                ('original_latitude', 'original_longitude'),
                'original_crs'
            )
        }),
        ('Dados Técnicos', {
            'fields': ('ne', 'nd', 'flow_rate', 'capacity')
        }),
    )

@admin.register(WaterWellUsage)
class WaterWellUsageAdmin(admin.ModelAdmin):
    list_display = ('water_well', 'date', 'water_usage', 'kwh_consumption')
    list_filter = ('water_well', 'date')
    search_fields = ('water_well__name', 'location')
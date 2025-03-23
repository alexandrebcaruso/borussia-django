from django.contrib import admin
from stats.models import WaterWell, WaterWellUsage

class WaterWellUserInline(admin.TabularInline):
    model = WaterWell.users.through
    extra = 0

class WaterWellAdmin(admin.ModelAdmin):
    inlines = [WaterWellUserInline]
    list_display = ('public_id', 'name', 'uf', 'locality', 'flow_rate', 'latitude', 'longitude')
    search_fields = ('public_id', 'name', 'locality')
    list_filter = ('uf', 'nature')

admin.site.register(WaterWell, WaterWellAdmin)
# admin.site.register(WaterWellUsage)


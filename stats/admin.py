from django.contrib import admin
from stats.models import WaterWell, WaterWellUsage, CustomUser

class WaterWellUserInline(admin.TabularInline):
    model = WaterWell.users.through
    extra = 0

class WaterWellAdmin(admin.ModelAdmin):
    inlines = [WaterWellUserInline]
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')
    list_filter = ('capacity',)

admin.site.register(WaterWell, WaterWellAdmin)

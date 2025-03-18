from django.shortcuts import render, get_object_or_404
from core.decorators import role_required
from stats.models import WaterWell, WaterWellUsage

@role_required('ApplicationAdmin')
def dashboard(request):
    water_wells = WaterWell.objects.all()
    return render(request, 'stats/dashboard.html', {
        'water_wells': water_wells
    })


@role_required('ApplicationAdmin')
def water_well_usage(request, well_id):
    water_well = get_object_or_404(WaterWell, id=well_id)
    usage_statistics = WaterWellUsage.objects.filter(water_well=water_well).order_by('-date')
    return render(request, 'stats/water_well_usage.html', {
        'water_well': water_well, 
        'usage_statistics': usage_statistics
    })
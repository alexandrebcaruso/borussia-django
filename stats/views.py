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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WaterWell

@csrf_exempt
def water_well_list(request):
    wells = WaterWell.objects.all().values(
        'public_id', 'name', 'uf', 'locality', 'nature', 'ne', 'nd', 'flow_rate', 'latitude', 'longitude', 'capacity'
    )
    return JsonResponse(list(wells), safe=False)

@csrf_exempt
def water_well_detail(request, public_id):
    well = WaterWell.objects.filter(public_id=public_id).values(
        'public_id', 'name', 'uf', 'locality', 'nature', 'ne', 'nd', 'flow_rate', 'latitude', 'longitude', 'capacity'
    )
    if well:
        return JsonResponse(well[0], safe=False)
    else:
        return JsonResponse({'error': 'Water well not found'}, status=404)
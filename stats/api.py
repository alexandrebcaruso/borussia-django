from django.http import JsonResponse
from stats.models import WaterWell
from django.core.serializers import serialize
import json

def wells_geojson(request):
    wells = WaterWell.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    
    features = []
    for well in wells:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [well.longitude, well.latitude]
            },
            "properties": {
                "id": well.public_id,
                "name": well.name,
                "uf": well.uf,
                "locality": well.locality,
                "nature": well.nature,
                "flow_rate": well.flow_rate,
                "ne": well.ne,
                "nd": well.nd,
                "capacity": well.capacity,
                "original_crs": well.original_crs,
                "details_url": f"/poco/{well.id}/"
            }
        })
    
    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    }, json_dumps_params={'ensure_ascii': False})
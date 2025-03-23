from django.http import JsonResponse
from stats.models import WaterWell

def wells_geojson(request):
    wells = WaterWell.objects.all()
    features = []
    for well in wells:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [well.longitude, well.latitude]
            },
            "properties": {
                "name": well.name,
                "uf": well.uf,
                "locality": well.locality,
                "flow_rate": well.flow_rate,
                "ne": well.ne,
                "nd": well.nd,
                "capacity": well.capacity,
                "current_month_usage": well.current_month_usage,
                "current_kwh_consumption": well.current_kwh_consumption
            }
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return JsonResponse(geojson)

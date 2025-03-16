from django.shortcuts import render, get_object_or_404
from .models import WaterClock, UsageStatistic
from core.decorators import role_required

@role_required('ApplicationAdmin')
def dashboard(request):
    water_clocks = WaterClock.objects.all().order_by('current_usage')
    return render(request, 'stats/dashboard.html', {'water_clocks': water_clocks})

@role_required('ApplicationAdmin')
def user_water_usage(request, user_id):
    water_clock = get_object_or_404(WaterClock, user_id=user_id)
    usage_statistics = UsageStatistic.objects.filter(water_clock=water_clock).order_by('-date')
    return render(request, 'stats/user_water_usage.html', {
        'water_clock': water_clock, 
        'usage_statistics': usage_statistics
        })

def my_water_usage(request):
    water_clock = WaterClock.objects.filter(user=request.user).first()
    if water_clock:
        current_usage = water_clock.current_usage
    else:
        current_usage = 0

    return render(request, 'stats/my_water_usage.html', {'current_usage': current_usage})
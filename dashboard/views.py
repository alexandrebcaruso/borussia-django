from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import WaterWell
from core.decorators import role_required

@login_required
@role_required('ApplicationAdmin')
def dashboard(request):
    water_wells = WaterWell.objects.all()
    return render(request, 'dashboard/dashboard.html', {'water_wells': water_wells})
from django.shortcuts import render
from .models import UsageStatistic  # Import your model

def dashboard(request):
    statistics = UsageStatistic.objects.all()  # Replace with actual query
    return render(request, 'aguastats/dashboard.html', {'statistics': statistics})
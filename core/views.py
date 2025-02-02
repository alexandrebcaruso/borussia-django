from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()
    
    return render(request, 'home.html', {'is_app_admin': is_app_admin})
    
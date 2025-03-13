from django.contrib.auth.decorators import login_required

def is_app_admin(request):
    if request.user.is_authenticated:
        is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()
    else:
        is_app_admin = False
    return {'is_app_admin': is_app_admin}
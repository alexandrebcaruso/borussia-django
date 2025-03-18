from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CustomUser
from payments.models import Payment

def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    return render(request, 'core/index.html', {'user_id': user_id})


def user_login(request):
    if request.user.is_authenticated:
        # Redirect logged-in users to a different page, e.g., the home page
        return redirect('index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # If the user is an app admin, ensure all regular users have a payment for the current month
            if user.roles.filter(name='ApplicationAdmin').exists():
                current_month = datetime.now().replace(day=1)  # Get the first day of the current month
                regular_users = CustomUser.objects.filter(roles__name='RegularUser')

                for regular_user in regular_users:
                    # Check if the user already has a payment for the current month
                    if not Payment.objects.filter(user=regular_user, month=current_month).exists():
                        # Create a payment for the current month
                        Payment.objects.create(
                            user=regular_user,
                            month=current_month,
                            status=Payment.AWAITING_PAYMENT  # Default status
                        )

            # Redirect based on user role
            if user.roles.filter(name='ApplicationAdmin').exists():
                return redirect('gestao_pagamentos')
            else:
                return redirect('meus_pagamentos')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'core/users/login.html')

def user_logout(request):
    logout(request)
    return redirect('entrar')


@login_required
def profile(request):

    if request.method == 'POST':
        user = request.user
        # Update the user's first name, last name, and phone number
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        messages.success(request, 'Seu perfil foi atualizado.')
        return redirect('perfil')

    return render(request, 'core/users/profile.html')

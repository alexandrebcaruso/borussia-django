from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from datetime import datetime
from django.utils import timezone

@login_required
def dashboard(request):
    # Get the current year
    current_year = timezone.now().year

    # Generate all months for the current year
    months_in_year = []
    for month in range(1, 13):
        months_in_year.append(datetime(current_year, month, 1))

    # Get all payments for the logged-in user
    payments = Payment.objects.filter(user=request.user)

    # Create a list of months with their payment status
    months = []
    for month in months_in_year:
        # Find payment for the current month
        payment = payments.filter(month__year=month.year, month__month=month.month).first()

        # Determine the status based on whether a payment exists
        if payment:
            status = 'Paid'
        else:
            status = 'Pending'

        # Add the month and status to the list
        months.append({
            'month': month.strftime('%B %Y'),
            'month_obj': month,  # Store the actual month object for link generation
            'status': status,
            'payment': payment,  # Pass the payment object if exists
        })
    
    # Create the context to pass to the template
    context = {
        'months': months,  # List of months with their status
        'today': datetime.today().date(),
    }
    
    return render(request, 'payments/dashboard.html', context)

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'payments/login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

from .forms import PaymentReceiptForm  # Assuming you have a form for the receipt

@login_required
def upload_receipt(request, year, month):
    # Create a datetime object from the provided year and month
    payment_date = datetime(year, month, 1)
    
    # Get or create a Payment object for the current user and the specific month
    payment, created = Payment.objects.get_or_create(
        user=request.user,
        month=payment_date,
        defaults={'status': 'pending'}  # Default status if no payment exists yet
    )
    
    # Handle the form submission for uploading the receipt
    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            payment.receipt = form.cleaned_data['receipt']
            payment.status = 'Paid'
            payment.save()
            return redirect('dashboard')
    else:
        form = PaymentReceiptForm()

    return render(request, 'payments/upload_receipt.html', {'form': form, 'payment': payment})


@login_required
def profile(request):
    # You can add any logic for the profile page here
    return render(request, 'payments/profile.html')

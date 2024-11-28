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

from .models import Payment
from .forms import PaymentReceiptForm
from django.contrib import messages

@login_required
def upload_receipt(request, year, month):
    payment_date = datetime(year, month, 1)  # Create the payment month object

    # Get or create the payment object for the user and month
    payment, created = Payment.objects.get_or_create(
        user=request.user,
        month=payment_date,
        defaults={'status': Payment.PENDING}
    )

    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            # Save the receipt
            form.save()

            # Update the status to awaiting approval
            payment.status = Payment.AWAITING_APPROVAL
            payment.save()

            messages.success(request, "Receipt uploaded successfully. Awaiting approval from the admin.")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error uploading the receipt. Please try again.")
    else:
        form = PaymentReceiptForm(instance=payment)

    return render(request, 'payments/upload_receipt.html', {'form': form, 'payment': payment})


@login_required
def profile(request):
    # You can add any logic for the profile page here
    return render(request, 'payments/profile.html')

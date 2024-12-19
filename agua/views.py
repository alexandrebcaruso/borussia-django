from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from agua.models import Payment, CustomUser
from .forms import PaymentReceiptForm
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

# TODO: move to new file, e.g., `decorators.py`
def role_required(role_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.roles.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to a permission denied page or login page
                return redirect('permission_denied')
        return _wrapped_view
    return decorator

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
        defaults={'status': Payment.AWAITING_APPROVAL}
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
    return render(request, 'users/profile.html')

@login_required
@role_required('ApplicationAdmin')
def users_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def manage_payments(request):
    # Get all payments that are awaiting approval
    payments = Payment.objects.filter(status=Payment.AWAITING_APPROVAL)

    if request.method == 'POST':
        payment_ids = request.POST.getlist('payment_ids')
        action = request.POST.get('action')

        for payment_id in payment_ids:
            payment = Payment.objects.get(id=payment_id)
            if action == 'approve':
                payment.status = Payment.PAID
                payment.approved_at = timezone.now()
            elif action == 'reject':
                payment.status = Payment.REJECTED
                payment.approved_at = None
            payment.save()

        return redirect('manage_payments')

    return render(request, 'payments/manage_payments.html', {'payments': payments})

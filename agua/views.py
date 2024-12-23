from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from agua.models import Payment, CustomUser
from .forms import PaymentReceiptForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.utils import timezone
from agua.decorators import role_required

def user_login(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = False
    if request.user.is_authenticated:
        is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.roles.filter(name='ApplicationAdmin').exists():
                return redirect('payment_list')
            else:
                return redirect('my_payments')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html', {'is_app_admin': is_app_admin})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@login_required
def home(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()

    # Redirect based on user role
    if is_app_admin:
        return redirect('payment_list')
    else:
        return redirect('my_payments')

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
            return redirect('my_payments')
        else:
            messages.error(request, "There was an error uploading the receipt. Please try again.")
    else:
        form = PaymentReceiptForm(instance=payment)

    return render(request, 'payments/upload_receipt.html', {'form': form, 'payment': payment})

@login_required
def profile(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Your profile has been updated.')
        return redirect('profile')

    return render(request, 'users/profile.html', {'is_app_admin': is_app_admin})

@role_required('ApplicationAdmin')
def users_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

@login_required
def my_payments(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()

    # Get the current year
    current_year = datetime.now().year

    # Generate all months for the current year
    months_in_year = []
    for month in range(1, 13):
        months_in_year.append(datetime(current_year, month, 1))

    # Ensure payments exist for each month of the current year
    for month in months_in_year:
        Payment.objects.get_or_create(
            user=request.user,
            month=month,
            defaults={'status': Payment.AWAITING_APPROVAL}
        )

    # Get all payments for the logged-in user for the current year
    payments = Payment.objects.filter(user=request.user, month__year=current_year)

    return render(request, 'users/my_payments.html', {'payments': payments, 'is_app_admin': is_app_admin})

@login_required
@role_required('ApplicationAdmin')
def payment_list(request):
    # Check if the user is an ApplicationAdmin
    is_app_admin = request.user.roles.filter(name='ApplicationAdmin').exists()

    # Get all payments awaiting approval
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

        return redirect('payment_list')

    return render(request, 'admin/payment_list.html', {'payments': payments, 'is_app_admin': is_app_admin})

@role_required('ApplicationAdmin')
def manage_payments(request):
    payments = Payment.objects.filter(status=Payment.AWAITING_APPROVAL)
    if request.method == 'POST':
        payment_ids = request.POST.getlist('payment_ids')
        action = request.POST.get('action')
        payments_to_update = Payment.objects.filter(id__in=payment_ids)
        if action == 'approve':
            payments_to_update.update(status=Payment.PAID, approved_at=timezone.now())
        elif action == 'reject':
            payments_to_update.update(status=Payment.REJECTED, approved_at=None)
        return redirect('manage_payments')
    return render(request, 'payments/manage_payments.html', {'payments': payments})

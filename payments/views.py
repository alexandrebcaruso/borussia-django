import os
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from core.decorators import role_required
from core.models import CustomUser
from payments.models import Payment
from .forms import PaymentReceiptForm

def home(request):
    return render(request, 'payments/home.html')

@login_required
def upload_receipt(request, year, month):
    payment_date = datetime(year, month, 1)  

    # Get or create the payment object for the user and month
    payment, created = Payment.objects.get_or_create(
        user=request.user,
        month=payment_date,
        defaults={'status': Payment.AWAITING_PAYMENT}  # Default status
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
            return redirect('meus_pagamentos')
        else:
            messages.error(request, "There was an error uploading the receipt. Please try again.")
    else:
        form = PaymentReceiptForm(instance=payment)

    return render(request, 'payments/payments/upload_receipt.html', {'form': form, 'payment': payment})

@login_required
def my_payments(request):
    # Get the current year
    current_year = datetime.now().year

    # Get the current month
    current_month = datetime.now().replace(day=1)  # Get the first day of the current month

    # Check if the user already has a payment for the current month
    payment = Payment.objects.filter(user=request.user, month=current_month).first()

    if not payment:
        # Create a payment for the current month
        Payment.objects.create(
            user=request.user,
            month=current_month,
            status=Payment.AWAITING_PAYMENT  # Default status
        )
    # Get all payments for the logged-in user for the current year
    payments = Payment.objects.filter(user=request.user, month__year=current_year)

    return render(request, 'payments/my_payments.html', {'payments': payments})

@login_required
@role_required('ApplicationAdmin')
def payment_list(request):
    # Handle POST request for actions
    if request.method == 'POST':
        payment_ids = request.POST.getlist('payment_ids')
        action = request.POST.get('action')
        payments_to_update = Payment.objects.filter(id__in=payment_ids)

        if action == 'approve':
            payments_to_update.update(status=Payment.PAID, approved_at=timezone.now())
            messages.success(request, "Selected payments have been approved.")
        elif action == 'reject':
            payments_to_update.update(status=Payment.REJECTED, approved_at=None)
            messages.success(request, "Selected payments have been rejected.")
        elif action == 'set_awaiting_payment':
            payments_to_update.update(status=Payment.AWAITING_PAYMENT, approved_at=None)
            messages.success(request, "Selected payments have been set to 'Awaiting Payment'.")
        elif action == 'set_awaiting_approval':
            payments_to_update.update(status=Payment.AWAITING_APPROVAL, approved_at=None)
            messages.success(request, "Selected payments have been set to 'Awaiting Approval'.")
        elif action == 'delete_receipt':
            for payment in payments_to_update:
                if payment.receipt:
                    if os.path.isfile(payment.receipt.path):
                        os.remove(payment.receipt.path)  # Delete the file from the filesystem
                    payment.receipt.delete()  # Delete the file reference from the database
                    payment.status = Payment.AWAITING_PAYMENT  # Set status to "awaiting_payment"
                    payment.save()
            messages.success(request, "Receipts for selected payments have been deleted.")
        return redirect('gestao_pagamentos')

    # Get all payments (default)
    payments = Payment.objects.all().order_by('-id')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        payments = payments.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        payments = payments.filter(status=status_filter)

    # Check if "Current Month" checkbox is selected (default behavior)
    current_month_only = request.GET.get('current_month', 'on') == 'on'

    # Check if a range of months is selected
    start_month = request.GET.get('start_month', '')
    end_month = request.GET.get('end_month', '')

    # If a range of months is selected, disable "Current Month"
    if start_month or end_month:
        current_month_only = False

    # Filter by current month if "Current Month" checkbox is selected
    if current_month_only:
        current_month = datetime.now().replace(day=1)  # Get the first day of the current month
        payments = payments.filter(month=current_month)
    else:
        # Filter by month or range of months
        if start_month:
            start_date = datetime.strptime(start_month, '%Y-%m').date()
            payments = payments.filter(month__gte=start_date)

        if end_month:
            end_date = datetime.strptime(end_month, '%Y-%m').date()
            payments = payments.filter(month__lte=end_date)

    # Pagination
    paginator = Paginator(payments, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'payments/payment_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'current_month_only': current_month_only,
        'start_month': start_month,
        'end_month': end_month,
    })

@login_required
@role_required('ApplicationAdmin')
def payment_history(request, user_id, year, month):
    user = CustomUser.objects.get(id=user_id)
    # Filter payments by user and the selected month
    payments = Payment.objects.filter(user=user, month__year=year, month__month=month).order_by('-month')
    # Create a datetime object for the selected month
    selected_month = datetime(year, month, 1)
    return render(request, 'payments/payment_history.html', {
        'user': user,
        'payments': payments,
        'selected_month': selected_month
    })

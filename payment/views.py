from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import ActivationRequest
from .models import RequestedPayment, PaymentHistory
from shop.models import Order
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

def staff_member_or_redirect(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))  # Replace 'profile' with the actual name of your profile URL pattern
    return _wrapped_view

@login_required
def request_payment(request):
    if request.method == "POST":
        today = timezone.now().date()
        # Ensure the current date is between the 1st and 27th, and the user has no existing requested payments
        if 1 <= today.day <= 7 and not RequestedPayment.objects.filter(user=request.user).exists():
            # Retrieve unpaid and delivered orders for the current user
            unpaid_delivered_orders = Order.objects.filter(user=request.user, profit_status='UNPAID', delivery_status='DELIVERED')
            
            if unpaid_delivered_orders.exists():
                # Create a new RequestedPayment instance
                requested_payment = RequestedPayment.objects.create(user=request.user)
                requested_payment.orders.set(unpaid_delivered_orders)
                
                # Calculate and update the total profit
                requested_payment.calculate_total_profit()
                
                messages.success(request, "Payment request has been created successfully.")
            else:
                messages.error(request, "No unpaid and delivered orders found to request payment.")
        else:
            messages.error(request, "Cannot request payment at this time or a request already exists.")
        
        return redirect(reverse('user_payment_history', kwargs={'username': request.user.username}))
    
    return redirect('home')

@staff_member_required
def requested_payments_list(request):
    if request.user.is_staff:
        requested_payments = RequestedPayment.objects.all()
    else:
        return redirect('home')
    return render(request, 'payment/payment_requests.html', {'requested_payments': requested_payments})

@staff_member_or_redirect
def pay(request, requested_payment_id):
    requested_payment = RequestedPayment.objects.get(id=requested_payment_id)
    orders = requested_payment.orders.all()

    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        trxid = request.POST.get('trxid')
        reference = request.POST.get('reference')
        amount = request.POST.get('amount')
        
        # Save PaymentHistory
        payment_history = PaymentHistory.objects.create(
            user=requested_payment.user,
            total_profit=amount,
            requested_date=requested_payment.requested_date,
            invoice_number=requested_payment.invoice_number,
            phone_number=phone_number,
            trxid=trxid,
            reference=reference,
        )
        payment_history.orders.set(orders)
        
        # Mark all associated orders as 'PAID'
        for order in orders:
            order.profit_status = 'PAID'
            order.save()
        
        # Delete the RequestedPayment instance
        requested_payment.delete()
        
        return redirect('payment_history')  # Redirect to a success page or the same page

    return render(request, 'payment/test.html', {'orders': orders})

@staff_member_or_redirect
def payment_history(request):
    payment_histories = PaymentHistory.objects.all().order_by('-date')  # Order by date, most recent first
    return render(request, 'payment/payment_history_admin.html', {'payment_histories': payment_histories})

@login_required
def user_payment_history(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user != user and not request.user.is_staff:
        return redirect('home')
    
    payment_histories = PaymentHistory.objects.filter(user=user).order_by('-date')
    
    # Check if there are any pending requested payments for the specified user
    pending_requested_payments = RequestedPayment.objects.filter(user=user)

    return render(request, 'payment/payment_history_user.html', {
        'payment_histories': payment_histories,
        'pending_requested_payments': pending_requested_payments,
    })

@staff_member_required
def manage_activation_requests(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not user_id:
            return HttpResponse("No user ID provided", status=400)

        try:
            user = get_object_or_404(User, id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User does not exist", status=404)

        user.reseller_status = 'active'  # Assuming 'active' is the correct status
        user.activation_date = timezone.now()
        user.expiry_date = user.activation_date + timedelta(days=365)
        user.save()

        # Delete the activation request for the user
        ActivationRequest.objects.filter(user=user).delete()

    # Always define activation_requests
    activation_requests = ActivationRequest.objects.all()
    context = {'activation_requests': activation_requests}
    return render(request, 'payment/mar.html', context)

@staff_member_required
def expired_active_users(request):
    # Get the current time
    now = timezone.now()

    # Query users whose reseller_status is 'active' and expiry_date is in the past
    expired_users = User.objects.filter(reseller_status=User.ACTIVE, expiry_date__lt=now)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            user.reseller_status = User.NOT_ACTIVE
            user.save()
            return redirect('expired_active_users')  # Redirect to the same view

    context = {'expired_users': expired_users}
    return render(request, 'payment/expired_active_users.html', context)

@login_required
def activation_request(request):
    if request.method == 'POST':
        trxid = request.POST.get('trxid')
        phone = request.POST.get('phone')
        reference = request.POST.get('reference')
        amount = request.POST.get('amount')

        activation_request = ActivationRequest.objects.create(
            user=request.user,
            trxid=trxid,
            phone=phone,
            reference=reference,
            amount=amount
        )
        return redirect('profile', username=request.user.username)
    return redirect('home')

@staff_member_required
def admintools(request):
    return render(request, 'payment/admintools.html')

@login_required
def generate_invoice_pdf(request, invoice_no):

    order = get_object_or_404(Order, invoice_no=invoice_no)
    user = order.user
    if request.user != user and not request.user.is_staff:
        return redirect('home')
    
    context = {
        'order': order,
        'total': order.sell_price*order.quantity,
    }
    return render(request, 'payment/invoice.html', context)



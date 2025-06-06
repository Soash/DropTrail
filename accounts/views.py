import random, string
from accounts.models import ActivationRequest
from shop.models import Order
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from payment.models import RequestedPayment
from django.core.exceptions import ValidationError

from django.conf import settings
from django.core.validators import validate_email

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user != user and not request.user.is_staff:
        return redirect('home')
    
    delivered_orders = Order.objects.filter(user=user, delivery_status='DELIVERED')
    paid_orders = delivered_orders.filter(profit_status='PAID')
    unpaid_orders = delivered_orders.filter(profit_status='UNPAID')
    
    total_sell = delivered_orders.aggregate(total_sell=Sum('sell_price'))['total_sell'] or 0
    total_profit = delivered_orders.aggregate(total_profit=Sum('profit'))['total_profit'] or 0
    paid_profit = paid_orders.aggregate(paid_profit=Sum('profit'))['paid_profit'] or 0
    unpaid_profit = unpaid_orders.aggregate(unpaid_profit=Sum('profit'))['unpaid_profit'] or 0
    
    orders = Order.objects.filter(user=user).order_by('-invoice_date')
    
    today = timezone.now().date()
    can_request_payment = 1 <= today.day <= 7 and not RequestedPayment.objects.filter(user=user).exists()
    pending_request = ActivationRequest.objects.filter(user=user).exists()
    
    return render(request, 'accounts/profile.html', {
        'user': user, 
        'orders': orders, 
        'total_sell': total_sell, 
        'total_profit': total_profit, 
        'paid_profit': paid_profit, 
        'unpaid_profit': unpaid_profit,
        'can_request_payment': can_request_payment,
        'pending_request': pending_request,
    })

def signup(request):
    if request.method == "POST":

        name = request.POST['name'].strip()
        pass1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        shopname = request.POST['shopname'].strip()
        email = request.POST['gmail'].strip() + '@gmail.com'
        phone = request.POST['phone'].strip()
        address = request.POST['address'].strip()

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid gmail address.")
            return redirect('signup')
        
        username = ''.join([char for char in name if char.isalpha()])
        original_username = username
        while User.objects.filter(username=username).exists():
            username = original_username + str(random.randint(1000, 9999))
        
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already registered!")
        #     return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = name
        user.shopname = shopname
        user.phone = phone
        user.address = address
        user.save()

        email_subject = "Confirmation Mail - bw.etrail.com.bd"
        template_name = 'accounts/mail_activation.html'
        send_email(user, request, user.email, email_subject, template_name, pass1)

        messages.success(request, "Please check your gmail.")
        return redirect('signin')

    return render(request, 'accounts/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile', username=username)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/signin.html')

def signout(request):
    logout(request)
    messages.error(request, "Sign out successfully.")
    return redirect('home')

def send_email(user, request, mail, email_subject, template_name, pass1):
    current_site = get_current_site(request)
    message = render_to_string(template_name, {
        'username': user.username,
        'pass': pass1,
        'domain': current_site.domain,
    })
    email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [mail],)
    email.fail_silently = True
    email.send()

@login_required
def update(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == 'POST':

        shopname = request.POST.get('shopname').strip()
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()

        user.shopname = shopname
        user.first_name = name
        user.phone = phone
        user.address = address
    
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile', user.username)

    return render(request, 'accounts/update.html', {'user': user})

def custom_404(request, exception):
    return render(request, 'accounts/404.html', {}, status=404)


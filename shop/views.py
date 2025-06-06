import random, string
from django.urls import reverse
from django.utils import timezone
from .models import Product, Category, Banner, Order
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


def none_redirect_view(request):
    return render(request, 'shop/none.html')

def home(request):
    categories = Category.objects.all()
    # banner = Banner.objects.all()
    # return render(request, 'shop/home.html', {'categories': categories, 'banner':banner})
    return render(request, 'shop/home.html', {'categories': categories,})

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category.html', {'category': category, 'products': products})

@login_required
def product(request, category_slug,  product_slug):

    if request.user.reseller_status == 'not_active':
        return redirect('profile', username=request.user.username)
    
    product = Product.objects.get(slug=product_slug)
    context = {'product': product}

    product_name = product.name
    product_price = product.price
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = int(request.POST.get('quantity'))

        # profit = int(request.POST.get('profit'))

        trxid = request.POST.get('trxid')
        bKash = request.POST.get('bKash')
        amount = request.POST.get('amount')
        reference = request.POST.get('reference')
        
        sell_price = int(request.POST.get('sell_price'))
     
        profit = int(sell_price) - int(product_price)
        profit = (profit*quantity)/2

        deliveryCharge = request.POST.get('deliveryCharge')

        today_min = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_max = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        existing_order = Order.objects.filter(
            phone=phone,
            user=request.user,
            order_status='PENDING',
            invoice_date__range=(today_min, today_max)
        ).exists()

        if existing_order:
            deliveryCharge = 0

        payment = request.POST.get('payment')
        if payment == 'adv':
            adv = 100
            cod = sell_price*quantity - int(adv) + int(deliveryCharge)
        elif payment == 'cash':
            adv = 0
            cod = sell_price*quantity+int(deliveryCharge)
        else:
            adv = sell_price*quantity+int(deliveryCharge)
            cod = 0

        invoice_no = generate_invoice_number()

        order = Order.objects.create(
            name=name,  phone=phone,
            address=address,
            user=request.user,
            product=product,
            product_name=product_name,
            product_price=product_price,
            profit = profit,
            sell_price = sell_price,
            quantity = quantity,
            adv = adv,
            cod = cod,
            delivery_charge = deliveryCharge,    
            trxid = trxid,
            bKash = bKash,
            amount = amount,
            reference = reference,
            invoice_no=invoice_no,
            invoice_date=timezone.now()
        )

        messages.success(request, "Order placed, please wait for confirmation.")
        return redirect('profile', username=request.user.username)

    return render(request, 'shop/product.html', context)

@staff_member_required
def all_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')
        delivery_status = request.POST.get('delivery_status')

        order = get_object_or_404(Order, id=order_id)
        if new_status:
            order.order_status = new_status
        if delivery_status:
            order.delivery_status = delivery_status
        order.save()
        return redirect('all_orders')

    orders = Order.objects.filter(delivery_status="PROCESSING").order_by('-invoice_date')
    return render(request, 'shop/allorders.html', {'orders': orders})

def generate_invoice_number():
    while True:
        invoice_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Order.objects.filter(invoice_no=invoice_no).exists():
            return invoice_no






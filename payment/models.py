from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from shop.models import Order
import random
import string

class RequestedPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Reseller")
    orders = models.ManyToManyField(Order, related_name="requested_payments")
    total_profit = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    requested_date = models.DateTimeField(default=timezone.now)
    invoice_number = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def calculate_total_profit(self):
        total = self.orders.aggregate(Sum('profit'))['profit__sum'] or 0
        self.total_profit = total
        self.save()

    def generate_invoice_number(self):
        while True:
            invoice_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not RequestedPayment.objects.filter(invoice_number=invoice_no).exists():
                self.invoice_number = invoice_no
                break

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.generate_invoice_number()
        super(RequestedPayment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Requested Payment {self.id} for {self.user}"

class PaymentHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Reseller")
    orders = models.ManyToManyField(Order)
    total_profit = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    requested_date = models.DateTimeField()
    invoice_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    trxid = models.CharField(max_length=100)
    reference = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment History {self.invoice_number} for {self.user}"


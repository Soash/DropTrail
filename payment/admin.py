from django.contrib import admin
from .models import RequestedPayment, PaymentHistory

@admin.register(RequestedPayment)
class RequestedPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_profit', 'requested_date')
    search_fields = ('user__username',)
    list_filter = ('requested_date',)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_profit', 'requested_date')


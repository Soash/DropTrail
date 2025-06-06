from django.urls import path
from . import views

urlpatterns = [
    path('request-payment/', views.request_payment, name='request_payment'),
    path('requested-payments/', views.requested_payments_list, name='requested_payments'),
    path('pay/<int:requested_payment_id>/', views.pay, name='pay'),

    path('payment-history/', views.payment_history, name='payment_history'),
    path('<str:username>/user-payment-history/', views.user_payment_history, name='user_payment_history'),

    path('activationrequest/', views.activation_request, name='requestA'),

    path('manageactivation/', views.manage_activation_requests, name='manage_activation_requests'),

    path('expired-active-users/', views.expired_active_users, name='expired_active_users'),

    path('admintools/', views.admintools, name='admintools'),

    path('download-invoice/<str:invoice_no>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
]




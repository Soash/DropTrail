from django.urls import path
from .views import contact_view, about_view, policy_view

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('policy/', policy_view, name='policy'),
]


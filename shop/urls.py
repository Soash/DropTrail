from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('None/', views.none_redirect_view, name='none_redirect'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('allorders/', views.all_orders, name='all_orders'),
]


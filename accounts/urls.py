from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('update/', views.update, name='update'),
    path('<str:username>/', views.profile, name='profile'),
]





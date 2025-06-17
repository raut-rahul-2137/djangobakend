from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('trading-config/', views.trading_config, name='trading_config'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('franchise/', views.franchise_submit, name='franchise_submit'),
] 
"""
URL configuration for PulariTraders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views

from django.urls import path,include

urlpatterns = [
 
    path('purchase/add/', views.add_purchase, name='add_purchase'),
    path('', views.dashboard, name='dashboard'),
    path('sale/add/', views.add_sale, name='add_sale'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/purchase/', views.purchase_report, name='purchase_report'),
    path('reports/customer/', views.customer_report, name='customer_report'),
    path('add/',views.add_feed, name='add_feed'),

    path('balance-sheet/', views.balance_sheet, name='balance_sheet'),
    path('ajax/feed-price/', views.get_feed_rate, name='get_feed_rate'),
    path('feeds/', views.feed_list, name='feed_list'),
    path('feed/update/<int:pk>/', views.update_feed, name='update_feed'),
    path('feed/delete/<int:pk>/', views.delete_feed, name='delete_feed'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/update/<int:pk>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:pk>/', views.delete_customer, name='delete_customer'),

]

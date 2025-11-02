from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Health check (no login required)
    path('health/', views.healthcheck, name='healthcheck'),
    path('healthcheck/', views.healthcheck, name='healthcheck_alt'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    
    # Transactions
    path('transactions/add/', views.transaction_create, name='transaction_create'),
]


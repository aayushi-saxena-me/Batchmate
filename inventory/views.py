from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
from datetime import timedelta
from .models import Product, Category, Supplier, Transaction
from .forms import ProductForm, CategoryForm, SupplierForm, TransactionForm


@login_required
def dashboard(request):
    """Dashboard view with inventory overview"""
    total_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(is_active=True, quantity__lte=F('reorder_level')).count()
    out_of_stock = Product.objects.filter(is_active=True, quantity=0).count()
    total_value = Product.objects.filter(is_active=True).aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0
    
    # Recent transactions
    recent_transactions = Transaction.objects.select_related('product').order_by('-created_at')[:10]
    
    # Low stock products
    low_stock_items = Product.objects.filter(
        is_active=True,
        quantity__lte=F('reorder_level')
    ).order_by('quantity')[:10]
    
    # Chart Data: Products by Category
    category_data = Category.objects.annotate(
        product_count=Count('product', filter=Q(product__is_active=True))
    ).filter(product_count__gt=0).values('name', 'product_count')
    category_labels = [cat['name'] for cat in category_data]
    category_counts = [cat['product_count'] for cat in category_data]
    
    # Chart Data: Stock Status Distribution
    in_stock_count = Product.objects.filter(is_active=True, quantity__gt=F('reorder_level')).count()
    low_stock_count = low_stock_products - out_of_stock if low_stock_products > out_of_stock else 0
    
    # Chart Data: Transaction Types (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    transaction_type_data = Transaction.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('transaction_type').annotate(
        count=Count('id')
    ).order_by('transaction_type')
    transaction_labels = [t['transaction_type'] for t in transaction_type_data]
    transaction_counts = [t['count'] for t in transaction_type_data]
    
    # Chart Data: Transaction Trends (last 30 days by date)
    from django.db import connection
    if connection.vendor == 'sqlite':
        # SQLite specific date extraction
        transaction_trends = Transaction.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            select={'day': "date(created_at, 'localtime')"}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
    else:
        # PostgreSQL/MySQL date extraction
        transaction_trends = Transaction.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
    
    trend_dates = []
    trend_counts = []
    for t in transaction_trends:
        if t['day']:
            try:
                if isinstance(t['day'], str):
                    from datetime import datetime
                    day_obj = datetime.strptime(t['day'], '%Y-%m-%d').date()
                else:
                    day_obj = t['day']
                trend_dates.append(day_obj.strftime('%m/%d'))
            except:
                trend_dates.append(str(t['day'])[:10])
            trend_counts.append(t['count'])
    
    # Chart Data: Top Products by Value
    top_products_by_value = Product.objects.filter(is_active=True).annotate(
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-total_value')[:10]
    top_product_names = [p.name[:20] + '...' if len(p.name) > 20 else p.name for p in top_products_by_value]
    top_product_values = [float(p.quantity * p.cost_price) for p in top_products_by_value]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'total_value': total_value,
        'recent_transactions': recent_transactions,
        'low_stock_items': low_stock_items,
        # Chart data (as JSON strings for safe template rendering)
        'category_labels': mark_safe(json.dumps(category_labels)),
        'category_counts': mark_safe(json.dumps(category_counts)),
        'in_stock_count': in_stock_count,
        'low_stock_count': low_stock_count,
        'transaction_labels': mark_safe(json.dumps(transaction_labels)),
        'transaction_counts': mark_safe(json.dumps(transaction_counts)),
        'trend_dates': mark_safe(json.dumps(trend_dates)),
        'trend_counts': mark_safe(json.dumps(trend_counts)),
        'top_product_names': mark_safe(json.dumps(top_product_names)),
        'top_product_values': mark_safe(json.dumps(top_product_values)),
    }
    return render(request, 'inventory/dashboard.html', context)


@login_required
def product_list(request):
    """List all products with search and filter"""
    products = Product.objects.filter(is_active=True).select_related('category', 'supplier')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Filter by stock status
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        products = products.filter(quantity__lte=F('reorder_level'))
    elif stock_filter == 'out':
        products = products.filter(quantity=0)
    
    # Ordering
    order_by = request.GET.get('order_by', 'name')
    products = products.order_by(order_by)
    
    # Pagination
    paginator = Paginator(products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
        'order_by': order_by,
    }
    return render(request, 'inventory/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    transactions = Transaction.objects.filter(product=product).order_by('-created_at')[:20]
    
    context = {
        'product': product,
        'transactions': transactions,
    }
    return render(request, 'inventory/product_detail.html', context)


@login_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add New Product'})


@login_required
def product_update(request, pk):
    """Update an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}'
    })


@login_required
def product_delete(request, pk):
    """Delete a product (soft delete by setting is_active=False)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
        return redirect('inventory:product_list')
    
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'inventory/category_form.html', {'form': form, 'title': 'Add New Category'})


@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_create(request):
    """Create a new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" created successfully!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {'form': form, 'title': 'Add New Supplier'})


@login_required
def transaction_create(request):
    """Create a new transaction"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Transaction processed successfully!')
            return redirect('inventory:product_detail', pk=transaction.product.pk)
    else:
        form = TransactionForm()
        product_id = request.GET.get('product')
        if product_id:
            try:
                form.fields['product'].initial = int(product_id)
            except ValueError:
                pass
    
    return render(request, 'inventory/transaction_form.html', {'form': form, 'title': 'Process Transaction'})


@csrf_exempt
def healthcheck(request):
    """
    Healthcheck endpoint to monitor application status.
    Accessible at /health/ or /healthcheck/
    Returns JSON with application health metrics.
    No login required, bypasses CSRF.
    """
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'request_info': {
            'host': request.get_host(),
            'method': request.method,
            'path': request.path,
        },
        'checks': {}
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = {
            'status': 'healthy',
            'message': 'Database connection successful'
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }
    
    # Check database tables exist
    try:
        Product.objects.exists()
        Category.objects.exists()
        Supplier.objects.exists()
        health_status['checks']['database_tables'] = {
            'status': 'healthy',
            'message': 'All required tables exist'
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['database_tables'] = {
            'status': 'unhealthy',
            'message': f'Table check failed: {str(e)}'
        }
    
    # Check environment variables (masked for security)
    env_vars = {
        'DEBUG': os.environ.get('DEBUG', 'Not set'),
        'DATABASE_URL': 'Set' if os.environ.get('DATABASE_URL') else 'Not set',
        'SECRET_KEY': 'Set' if os.environ.get('SECRET_KEY') else 'Not set',
        'ALLOWED_HOSTS': list(settings.ALLOWED_HOSTS) if hasattr(settings, 'ALLOWED_HOSTS') else 'Not set',
        'CSRF_TRUSTED_ORIGINS': list(settings.CSRF_TRUSTED_ORIGINS) if hasattr(settings, 'CSRF_TRUSTED_ORIGINS') else [],
        'HOST_MATCH': request.get_host() in settings.ALLOWED_HOSTS if hasattr(settings, 'ALLOWED_HOSTS') else False,
    }
    health_status['checks']['environment'] = {
        'status': 'healthy',
        'message': 'Environment variables checked',
        'variables': env_vars
    }
    
    # Check static files
    try:
        static_root = settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else None
        health_status['checks']['static_files'] = {
            'status': 'healthy',
            'message': 'Static files configured',
            'static_root': str(static_root) if static_root else 'Not set'
        }
    except Exception as e:
        health_status['checks']['static_files'] = {
            'status': 'warning',
            'message': f'Static files check: {str(e)}'
        }
    
    # Return JSON response
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)


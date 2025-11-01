from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator
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
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'total_value': total_value,
        'recent_transactions': recent_transactions,
        'low_stock_items': low_stock_items,
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


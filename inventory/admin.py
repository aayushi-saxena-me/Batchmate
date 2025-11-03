from django.contrib import admin
from .models import Category, Supplier, Product, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'created_by']
    
    def get_queryset(self, request):
        """Filter categories to show only user's own categories"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        """Set created_by to current user when creating"""
        if not change:  # Creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_by', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at', 'created_by']
    
    def get_queryset(self, request):
        """Filter suppliers to show only user's own suppliers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        """Set created_by to current user when creating"""
        if not change:  # Creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'quantity', 'selling_price', 'stock_status', 'is_active', 'created_by', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'created_by']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['created_at', 'updated_at', 'stock_status', 'is_low_stock']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sku', 'category', 'supplier', 'image')
        }),
        ('Inventory', {
            'fields': ('quantity', 'reorder_level', 'stock_status', 'is_low_stock')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'profit_margin')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Filter products to show only user's own products"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        """Set created_by to current user when creating"""
        if not change:  # Creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit foreign key choices to user's data"""
        if db_field.name == "category":
            if not request.user.is_superuser:
                kwargs["queryset"] = Category.objects.filter(created_by=request.user)
        elif db_field.name == "supplier":
            if not request.user.is_superuser:
                kwargs["queryset"] = Supplier.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def stock_status(self, obj):
        return obj.stock_status
    stock_status.short_description = 'Stock Status'

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'reference', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'created_at', 'created_by']
    search_fields = ['product__name', 'reference', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """Filter transactions to show only user's own transactions"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        """Set created_by to current user when creating"""
        if not change:  # Creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit foreign key choices to user's data"""
        if db_field.name == "product":
            if not request.user.is_superuser:
                kwargs["queryset"] = Product.objects.filter(created_by=request.user, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


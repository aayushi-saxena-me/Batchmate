from django.contrib import admin
from .models import Category, Supplier, Product, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'quantity', 'selling_price', 'stock_status', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
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
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['product__name', 'reference', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Product, Category, Supplier, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'sku', 'category', 'supplier',
            'quantity', 'reorder_level', 'cost_price', 'selling_price', 'image', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limit category and supplier choices to user's data
        if user:
            self.fields['category'].queryset = Category.objects.filter(created_by=user)
            self.fields['supplier'].queryset = Supplier.objects.filter(created_by=user)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('sku', css_class='form-group col-md-6 mb-0'),
            ),
            'description',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('supplier', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('quantity', css_class='form-group col-md-4 mb-0'),
                Column('reorder_level', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('cost_price', css_class='form-group col-md-6 mb-0'),
                Column('selling_price', css_class='form-group col-md-6 mb-0'),
            ),
            'image',
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'description',
        )


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Row(
                Column('contact_person', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
            ),
            'email',
            'address',
        )


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'transaction_type', 'quantity', 'reference', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limit product choices to user's products
        if user:
            self.fields['product'].queryset = Product.objects.filter(created_by=user, is_active=True)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('transaction_type', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('quantity', css_class='form-group col-md-6 mb-0'),
                Column('reference', css_class='form-group col-md-6 mb-0'),
            ),
            'notes',
        )


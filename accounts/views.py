from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with crispy forms"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Register', css_class='btn btn-primary')
        )


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with crispy forms"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn btn-primary w-100')
        )


def register_view(request):
    """User registration view"""
    # Safely check authentication
    try:
        is_authenticated = request.user.is_authenticated
    except Exception:
        is_authenticated = False
    
    if is_authenticated:
        return redirect('inventory:dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view with error handling"""
    # Safely check authentication - don't fail if database is unavailable
    try:
        is_authenticated = request.user.is_authenticated
    except Exception:
        # If database check fails, assume not authenticated
        is_authenticated = False
    
    if is_authenticated:
        return redirect('inventory:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('inventory:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def is_superuser(user):
    """Check if user is a superuser"""
    return user.is_authenticated and user.is_superuser


class SuperuserCreationForm(forms.ModelForm):
    """Form for creating superusers (admin only)"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Password must be at least 8 characters.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Enter the same password as before, for verification.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('is_staff', css_class='form-group col-md-6 mb-0'),
                Column('is_superuser', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Create User', css_class='btn btn-primary')
        )
        # Set default values
        self.fields['is_staff'].initial = True
        self.fields['is_superuser'].initial = True
        self.fields['is_staff'].help_text = 'Allow access to Django admin panel'
        self.fields['is_superuser'].help_text = 'Full administrative privileges'
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


@login_required
@user_passes_test(is_superuser)
def create_superuser_view(request):
    """View for creating superusers (admin only)"""
    if request.method == 'POST':
        form = SuperuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_type = 'superuser' if user.is_superuser else 'staff user' if user.is_staff else 'user'
            messages.success(request, f'{user_type.capitalize()} "{username}" created successfully!')
            return redirect('accounts:create_superuser')
    else:
        form = SuperuserCreationForm()
    
    # Get list of existing superusers for reference
    existing_superusers = User.objects.filter(is_superuser=True).order_by('-date_joined')
    existing_staff = User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')
    
    context = {
        'form': form,
        'existing_superusers': existing_superusers,
        'existing_staff': existing_staff,
    }
    
    return render(request, 'accounts/create_superuser.html', context)


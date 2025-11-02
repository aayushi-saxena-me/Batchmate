from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


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


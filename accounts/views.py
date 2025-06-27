from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import User, Admin, Address
from .forms import UserRegistrationForm, UserLoginForm
from accounts.decorators import superadmin_required
from products.models import Product


# User Views
def login_view(request):
    """Authenticate and log in a user."""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')  # redirect to home
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Handle user registration form and create a new user account."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect('login')


@login_required
def view_profile(request):
    return render(request, 'accounts/view_profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        request.user.name = name
        request.user.phone_number = phone
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('view_profile')

    return render(request, 'accounts/edit_profile.html', {'user': request.user})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully.')
        return redirect('view_profile')

    return render(request, 'accounts/change_password.html')

@login_required
def add_address(request):
    if request.method == 'POST':
        street = request.POST.get('street_address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        Address.objects.create(
            user=request.user,
            street_address=street,
            city=city,
            province=province,
            country=country,
            zip_code=zip_code
        )

        messages.success(request, 'Address added successfully.')
        return redirect('manage_addresses')

    return render(request, 'accounts/add_address.html')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.street_address = request.POST.get('street_address')
        address.city = request.POST.get('city')
        address.province = request.POST.get('province')
        address.country = request.POST.get('country')
        address.zip_code = request.POST.get('zip_code')
        address.save()

        messages.success(request, 'Address updated successfully.')
        return redirect('manage_addresses')

    return render(request, 'accounts/edit_address.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully.')
        return redirect('manage_addresses')

    return render(request, 'accounts/confirm_delete_address.html', {'address': address})

@login_required
def manage_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/manage_addresses.html', {'addresses': addresses})


# Superadmin Login View
def superadmin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):
                request.session['superadmin_id'] = admin.id
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except Admin.DoesNotExist:
            messages.error(request, 'Superadmin not found.')
    return render(request, 'accounts/superadmin_login.html')

# Superadmin Logout View
def superadmin_logout_view(request):
    request.session.flush()
    return redirect('superadmin_login')

# Admin Dashboard View
@superadmin_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Admin
from .forms import UserRegistrationForm, UserLoginForm, AdminLoginForm
from accounts.decorators import superadmin_required


# User Views
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('user_home')
                else:
                    messages.error(request, 'Invalid password')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from products.models import Product

@login_required
def user_home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'accounts/user_home.html', {'products': products})


@login_required
def view_profile(request):
    return render(request, 'accounts/view_profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')

        request.user.name = name
        request.user.phone_number = phone
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('view_profile')

    return render(request, 'accounts/edit_profile.html', {'user': request.user})

from django.contrib.auth import update_session_auth_hash

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



from .models import Address

@login_required
def manage_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/manage_addresses.html', {'addresses': addresses})


# Admin Views
def superadmin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(email=email)

            if check_password(password, admin.password):
                # Save superadmin session
                request.session['superadmin_id'] = admin.id
                return redirect('admin_dashboard')  # Replace with your actual dashboard route
            else:
                messages.error(request, 'Invalid credentials or not a superadmin.')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials or not a superadmin.')

    return render(request, 'accounts/superadmin_login.html')


def superadmin_logout_view(request):
    try:
        del request.session['superadmin_id']
    except KeyError:
        pass
    return redirect('superadmin_login')

@superadmin_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')







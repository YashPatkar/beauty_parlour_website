"""
Accounts app - Registration, Login, Logout, Profile (detailed: avatar, name, email, saved payment methods).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Profile
from .forms import RegisterForm


def register_view(request):
    """Register new user with optional email and profile picture, then auto-login and redirect to home."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
                profile.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Login using authenticate() and login(). Redirect to home on success."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout user and redirect to home."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    """Detailed profile: avatar, name, email, phone, saved payment methods. Update and add card."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    # Update profile (name, email, phone, avatar)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            if email:
                user.email = email
            user.save()
            profile.phone = request.POST.get('phone', '').strip()
            profile.save()
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
                profile.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        if action == 'add_card':
            last_four = request.POST.get('last_four', '').strip()[:4]
            card_type = request.POST.get('card_type', 'visa')
            nickname = request.POST.get('nickname', '').strip()
            if last_four and len(last_four) == 4 and last_four.isdigit():
                from payments.models import SavedPaymentMethod
                # If first card, set as default
                existing = SavedPaymentMethod.objects.filter(user=user)
                is_default = not existing.exists()
                SavedPaymentMethod.objects.create(
                    user=user, last_four=last_four, card_type=card_type,
                    nickname=nickname or f"Card ****{last_four}", is_default=is_default
                )
                messages.success(request, 'Payment method added (demo).')
            else:
                messages.error(request, 'Enter valid last 4 digits.')
            return redirect('profile')

    from payments.models import SavedPaymentMethod
    saved_methods = SavedPaymentMethod.objects.filter(user=user)
    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'saved_methods': saved_methods,
    })


@login_required
def remove_saved_method_view(request, pk):
    """Remove a saved payment method (demo)."""
    from payments.models import SavedPaymentMethod
    method = get_object_or_404(SavedPaymentMethod, pk=pk, user=request.user)
    method.delete()
    messages.success(request, 'Payment method removed.')
    return redirect('profile')


@login_required
def set_default_card_view(request, pk):
    """Set a saved card as default."""
    from payments.models import SavedPaymentMethod
    method = get_object_or_404(SavedPaymentMethod, pk=pk, user=request.user)
    SavedPaymentMethod.objects.filter(user=request.user).update(is_default=False)
    method.is_default = True
    method.save()
    messages.success(request, 'Default card updated.')
    return redirect('profile')

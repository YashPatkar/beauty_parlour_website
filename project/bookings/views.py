"""
Bookings app - Book appointment, My Appointments, Booking history, Cart, Favourites.
Protected with @login_required for user-only features.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date

from services.models import Service, Staff
from .models import Appointment, Cart, CartItem, UserFavourite


@login_required
def booking_view(request, service_id):
    """Booking page - select date, time; prevent same user same slot clash."""
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    staff_list = Staff.objects.filter(is_active=True)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        staff_id = request.POST.get('staff') or None
        notes = request.POST.get('notes', '').strip()

        if not date_str or not time_str:
            messages.error(request, 'Please select date and time.')
            return render(request, 'bookings/booking.html', {
                'service': service,
                'staff_list': staff_list,
            })

        try:
            appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appt_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid date or time.')
            return render(request, 'bookings/booking.html', {
                'service': service,
                'staff_list': staff_list,
            })

        if appt_date < date.today():
            messages.error(request, 'Cannot book in the past.')
            return render(request, 'bookings/booking.html', {
                'service': service,
                'staff_list': staff_list,
            })

        # Simple clash: same user, same date, same time (any service)
        clash = Appointment.objects.filter(
            user=request.user,
            date=appt_date,
            time=appt_time,
            status__in=['pending', 'confirmed']
        ).exists()
        if clash:
            messages.error(request, 'You already have an appointment at this date and time.')
            return render(request, 'bookings/booking.html', {
                'service': service,
                'staff_list': staff_list,
            })

        staff = None
        if staff_id:
            staff = Staff.objects.filter(pk=staff_id, is_active=True).first()

        appointment = Appointment.objects.create(
            user=request.user,
            service=service,
            staff=staff,
            date=appt_date,
            time=appt_time,
            notes=notes,
            status='pending',
        )
        messages.success(request, 'Appointment booked! Proceed to payment.')
        return redirect('payment', appointment.id)

    return render(request, 'bookings/booking.html', {
        'service': service,
        'staff_list': staff_list,
    })


@login_required
def my_appointments_view(request):
    """List current user's appointments: Upcoming and Booking history (past/completed/cancelled)."""
    today = date.today()
    all_appointments = Appointment.objects.filter(user=request.user).select_related(
        'service', 'staff'
    ).order_by('-date', '-time')
    # Upcoming: pending/confirmed with date >= today
    upcoming_appointments = [
        a for a in all_appointments
        if a.status in ('pending', 'confirmed') and (a.date > today or (a.date == today and a.time))
    ]
    # History: completed, cancelled, or past date
    past_appointments = [
        a for a in all_appointments
        if a not in upcoming_appointments
    ]
    return render(request, 'bookings/my_appointments.html', {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    })


@login_required
def cancel_appointment_view(request, appointment_id):
    """Cancel an appointment if it is still pending/confirmed."""
    appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)
    if appointment.status in ('pending', 'confirmed'):
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
    else:
        messages.warning(request, 'This appointment cannot be cancelled.')
    return redirect('my_appointments')


# ---------- Cart (add to cart, view cart, remove) ----------
@login_required
def cart_view(request):
    """View cart with total price."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('service').all()
    total = cart.total_price()
    return render(request, 'bookings/cart.html', {'cart': cart, 'items': items, 'total': total})


@login_required
def add_to_cart_view(request, service_id):
    """Add a service to cart (quantity 1 or increment)."""
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, service=service, defaults={'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'Added {service.name} to cart.')
    next_target = request.GET.get('next')
    if next_target == 'cart':
        return redirect('cart')
    ref = request.META.get('HTTP_REFERER')
    return redirect(ref if ref else 'cart')


@login_required
def remove_from_cart_view(request, service_id):
    """Remove a service from cart."""
    cart = get_object_or_404(Cart, user=request.user)
    item = cart.items.filter(service_id=service_id).first()
    if item:
        item.delete()
        messages.success(request, 'Removed from cart.')
    return redirect('cart')


# ---------- Favourites (saved list, add, remove) ----------
@login_required
def saved_list_view(request):
    """View saved services (favourites) for quick book."""
    favourites = UserFavourite.objects.filter(user=request.user).select_related('service').order_by('-created_at')
    return render(request, 'bookings/saved_list.html', {'favourites': favourites})


@login_required
def add_to_favourites_view(request, service_id):
    """Save a service to favourites."""
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    _, created = UserFavourite.objects.get_or_create(user=request.user, service=service)
    if created:
        messages.success(request, f'Saved {service.name} to your list.')
    if request.GET.get('next') == 'saved_list':
        return redirect('saved_list')
    ref = request.META.get('HTTP_REFERER')
    return redirect(ref if ref else 'saved_list')


@login_required
def remove_from_favourites_view(request, service_id):
    """Remove a service from favourites."""
    UserFavourite.objects.filter(user=request.user, service_id=service_id).delete()
    messages.success(request, 'Removed from saved list.')
    ref = request.META.get('HTTP_REFERER')
    return redirect(ref if ref else 'saved_list')

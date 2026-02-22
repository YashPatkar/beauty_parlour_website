"""
Custom Admin Panel - separate from Django Admin.
Login via ADMIN_PANEL_USERNAME and ADMIN_PANEL_PASSWORD from .env (read in settings).
Session-based; no Django superuser.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from services.models import Service, Staff
from bookings.models import Appointment
from payments.models import Payment


def _panel_logged_in(request):
    """Check if custom admin panel session is active."""
    return request.session.get('admin_panel_logged_in') is True


def panel_login_view(request):
    """Admin panel login - check credentials from settings (loaded from .env)."""
    if _panel_logged_in(request):
        return redirect('dashboard_home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if (username == getattr(settings, 'ADMIN_PANEL_USERNAME', '') and
                password == getattr(settings, 'ADMIN_PANEL_PASSWORD', '')):
            request.session['admin_panel_logged_in'] = True
            return redirect('dashboard_home')
        error = 'Invalid username or password.'
    return render(request, 'dashboard/panel_login.html', {'error': error})


def panel_logout_view(request):
    """Clear admin panel session."""
    request.session.pop('admin_panel_logged_in', None)
    return redirect('panel_login')


def _require_panel(view_func):
    """Decorator: redirect to panel login if not logged in to panel."""
    def wrapper(request, *args, **kwargs):
        if not _panel_logged_in(request):
            return redirect('panel_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@_require_panel
def dashboard_home_view(request):
    """Dashboard home - totals for users, bookings, services, payments."""
    from django.db.models import Count
    total_users = User.objects.count()
    total_bookings = Appointment.objects.count()
    total_services = Service.objects.filter(is_active=True).count()
    total_payments = Payment.objects.filter(status='paid').count()
    return render(request, 'dashboard/dashboard_home.html', {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_services': total_services,
        'total_payments': total_payments,
    })


# --- Services CRUD ---
@_require_panel
def manage_services_view(request):
    services = Service.objects.all().order_by('name')
    return render(request, 'dashboard/manage_services.html', {'services': services})


@_require_panel
def service_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0')
        duration = request.POST.get('duration', '60')
        image_url = request.POST.get('image_url', '').strip()
        location = request.POST.get('location', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if name and price:
            try:
                Service.objects.create(
                    name=name, description=description,
                    price=price, duration_minutes=int(duration or 60),
                    image_url=image_url or '', location=location or '', is_active=is_active
                )
                return redirect('manage_services')
            except (ValueError, TypeError):
                pass
    return render(request, 'dashboard/service_form.html', {'service': None})


@_require_panel
def service_edit_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.name = request.POST.get('name', '').strip() or service.name
        service.description = request.POST.get('description', '').strip()
        service.image_url = request.POST.get('image_url', '').strip()
        service.location = request.POST.get('location', '').strip()
        try:
            service.price = request.POST.get('price', service.price)
            service.duration_minutes = int(request.POST.get('duration') or service.duration_minutes)
        except (ValueError, TypeError):
            pass
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()
        return redirect('manage_services')
    return render(request, 'dashboard/service_form.html', {'service': service})


@_require_panel
def location_suggestions_view(request):
    """JSON API: suggest locations (from existing services) matching query. Used with debounce."""
    q = (request.GET.get('q') or '').strip()[:50]
    if not q:
        return JsonResponse({'locations': []})
    locations = list(
        Service.objects.filter(location__icontains=q)
        .exclude(location='')
        .values_list('location', flat=True)
        .distinct()[:15]
    )
    return JsonResponse({'locations': locations})


@_require_panel
def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('manage_services')
    return render(request, 'dashboard/confirm_delete.html', {
        'title': 'Delete Service',
        'object_name': service.name,
        'cancel_url': 'manage_services',
    })


# --- Staff CRUD ---
@_require_panel
def manage_staff_view(request):
    staff_list = Staff.objects.all().order_by('name')
    return render(request, 'dashboard/manage_staff.html', {'staff_list': staff_list})


@_require_panel
def staff_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        specialization = request.POST.get('specialization', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if name:
            Staff.objects.create(
                name=name, specialization=specialization,
                image_url=image_url or '', is_active=is_active
            )
            return redirect('manage_staff')
    return render(request, 'dashboard/staff_form.html', {'staff': None})


@_require_panel
def staff_edit_view(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.name = request.POST.get('name', '').strip() or staff.name
        staff.specialization = request.POST.get('specialization', '').strip()
        staff.image_url = request.POST.get('image_url', '').strip()
        staff.is_active = request.POST.get('is_active') == 'on'
        staff.save()
        return redirect('manage_staff')
    return render(request, 'dashboard/staff_form.html', {'staff': staff})


@_require_panel
def staff_delete_view(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('manage_staff')
    return render(request, 'dashboard/confirm_delete.html', {
        'title': 'Delete Staff',
        'object_name': staff.name,
        'cancel_url': 'manage_staff',
    })


# --- Appointments list (view only; optional edit status) ---
@_require_panel
def manage_appointments_view(request):
    appointments = Appointment.objects.select_related('user', 'service', 'staff').order_by('-date', '-time')
    return render(request, 'dashboard/manage_appointments.html', {'appointments': appointments})


@_require_panel
def appointment_delete_view(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.delete()
        return redirect('manage_appointments')
    return render(request, 'dashboard/confirm_delete.html', {
        'title': 'Delete Appointment',
        'object_name': f"{appt.service.name} - {appt.date}",
        'cancel_url': 'manage_appointments',
    })


# --- Payments list ---
@_require_panel
def manage_payments_view(request):
    payments = Payment.objects.select_related('appointment').order_by('-created_at')
    return render(request, 'dashboard/manage_payments.html', {'payments': payments})

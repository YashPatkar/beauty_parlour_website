"""
Services app - Homepage, Services list, Service detail, Contact, Feedback, 404.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service, Staff, Feedback, Contact

# Optional image URLs for /services/ – matched by service name (case-insensitive substring).
SERVICE_IMAGE_URLS = [
    ('facial', 'https://img.freepik.com/premium-photo/young-beautiful-woman-is-receiving-facials-skincare-treatments-beauty-parlour_1218867-48453.jpg'),
    ('hair color', 'https://img.freepik.com/premium-photo/young-beautiful-woman-is-receiving-hair-coloring-service-beauty-parlour_1218867-42504.jpg'),
    ('hair colour', 'https://img.freepik.com/premium-photo/young-beautiful-woman-is-receiving-hair-coloring-service-beauty-parlour_1218867-42504.jpg'),
    ('bridal', 'https://img.freepik.com/premium-photo/indian-bride-makeup-session-with-professional-artist-makeup-artist-touching-up-indian-bride_1284935-3688.jpg'),
    ('haircut', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRycYPswmagqysl-gIJ3D5xgYNvWeFTHBnVfA&s'),
    ('styling', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRycYPswmagqysl-gIJ3D5xgYNvWeFTHBnVfA&s'),
    ('manicure', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMqxMcGb3BMgluJqutjQZ8CvFlkHkcVmTjFQ&s'),
    ('pedicure', 'https://img.freepik.com/premium-photo/manicure-pedicure-beauty-salon-concept-womans-feet-with-cotton-flower_926199-2997825.jpg?semt=ais_user_personalization&w=740&q=80'),
]


def get_service_display_image_url(service):
    """Return service.image_url if set, else keyword match from SERVICE_IMAGE_URLS, else None."""
    if service.image_url:
        return service.image_url
    name_lower = (service.name or '').lower()
    for keyword, url in SERVICE_IMAGE_URLS:
        if keyword in name_lower:
            return url
    return None


def _attach_display_image_urls(services):
    """Attach display_image_url on each service (list or single)."""
    for s in (services if hasattr(services, '__iter__') and not isinstance(services, (str, dict)) else [services]):
        setattr(s, 'display_image_url', get_service_display_image_url(s))


def home_view(request):
    """Homepage - show featured services, team, testimonials for landing sections."""
    services = Service.objects.filter(is_active=True)[:6]
    services_latest = Service.objects.filter(is_active=True)[:3]
    _attach_display_image_urls(services)
    _attach_display_image_urls(services_latest)
    staff_list = Staff.objects.filter(is_active=True)[:4]
    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, 'services/home.html', {
        'services': services,
        'services_latest': services_latest,
        'staff_list': staff_list,
        'feedbacks': feedbacks,
    })


def services_list_view(request):
    """Services + Gallery combined page. Optional search by name, description, location."""
    services = Service.objects.filter(is_active=True)
    q = (request.GET.get('q') or '').strip()
    if q:
        services = services.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q)
        )
    _attach_display_image_urls(services)
    return render(request, 'services/services_gallery.html', {'services': services, 'search_query': q})


def service_detail_view(request, pk):
    """Service detail page - includes staff list and OpenStreetMap."""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    _attach_display_image_urls(service)
    staff_list = Staff.objects.filter(is_active=True)
    return render(request, 'services/service_detail.html', {'service': service, 'staff_list': staff_list})


def contact_view(request):
    """Contact form - POST saves to Contact; redirects to about#contact. GET redirects to about#contact."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            return redirect(reverse('about') + '?sent=1#contact')
    return redirect(reverse('about') + '#contact')


@login_required
def feedback_view(request):
    """Submit feedback - rating and message, stored with user."""
    if request.method == 'POST':
        rating = request.POST.get('rating', '5')
        message = request.POST.get('message', '').strip()
        try:
            r = int(rating)
            if 1 <= r <= 5:
                Feedback.objects.create(user=request.user, rating=r, message=message)
                return redirect('home')
        except ValueError:
            pass
    return render(request, 'services/feedback.html')


def about_view(request):
    return render(request, 'services/about.html')


def team_view(request):
    staff_list = Staff.objects.filter(is_active=True)
    return render(request, 'services/team.html', {'staff_list': staff_list})


def gallery_view(request):
    """Redirect to combined Services & Gallery page, gallery section."""
    return redirect(reverse('services_list') + '#gallery')


def offers_view(request):
    services = Service.objects.filter(is_active=True)[:6]
    _attach_display_image_urls(services)
    return render(request, 'services/offers.html', {'services': services})


def faq_view(request):
    return render(request, 'services/faq.html')


def testimonials_view(request):
    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')[:10]
    return render(request, 'services/testimonials.html', {'feedbacks': feedbacks})


def privacy_view(request):
    return render(request, 'services/privacy.html')


def terms_view(request):
    return render(request, 'services/terms.html')


def page_not_found(request, exception=None):
    """Custom 404 page for any unknown URL (e.g. /dhasdhasdh, typos). handler404 in config/urls.py."""
    return render(request, 'services/404.html', status=404)

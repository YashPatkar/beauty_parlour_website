from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_list_view, name='services_list'),
    path('services/<int:pk>/', views.service_detail_view, name='service_detail'),
    path('about/', views.about_view, name='about'),
    path('team/', views.team_view, name='team'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('offers/', views.offers_view, name='offers'),
    path('faq/', views.faq_view, name='faq'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('feedback/', views.feedback_view, name='feedback'),
    # Catch-all: show custom 404 even when DEBUG=True (Django otherwise shows debug 404 page)
    re_path(r'^.+$', views.page_not_found),
]

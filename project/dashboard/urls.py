from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_login_view, name='panel_login'),
    path('logout/', views.panel_logout_view, name='panel_logout'),
    path('home/', views.dashboard_home_view, name='dashboard_home'),
    path('services/', views.manage_services_view, name='manage_services'),
    path('services/add/', views.service_add_view, name='service_add'),
    path('services/location-suggestions/', views.location_suggestions_view, name='location_suggestions'),
    path('services/<int:pk>/edit/', views.service_edit_view, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete_view, name='service_delete'),
    path('staff/', views.manage_staff_view, name='manage_staff'),
    path('staff/add/', views.staff_add_view, name='staff_add'),
    path('staff/<int:pk>/edit/', views.staff_edit_view, name='staff_edit'),
    path('staff/<int:pk>/delete/', views.staff_delete_view, name='staff_delete'),
    path('appointments/', views.manage_appointments_view, name='manage_appointments'),
    path('appointments/<int:pk>/delete/', views.appointment_delete_view, name='appointment_delete'),
    path('payments/', views.manage_payments_view, name='manage_payments'),
]

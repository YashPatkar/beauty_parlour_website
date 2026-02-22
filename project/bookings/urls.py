from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.booking_view, name='booking'),
    path('my-appointments/', views.my_appointments_view, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment_view, name='cancel_appointment'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:service_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:service_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('saved/', views.saved_list_view, name='saved_list'),
    path('saved/add/<int:service_id>/', views.add_to_favourites_view, name='add_to_favourites'),
    path('saved/remove/<int:service_id>/', views.remove_from_favourites_view, name='remove_from_favourites'),
]

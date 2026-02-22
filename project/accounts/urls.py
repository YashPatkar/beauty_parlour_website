from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/payment-method/<int:pk>/remove/', views.remove_saved_method_view, name='remove_saved_method'),
    path('profile/payment-method/<int:pk>/default/', views.set_default_card_view, name='set_default_card'),
]

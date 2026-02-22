from django.urls import path
from . import views

urlpatterns = [
    path('<int:appointment_id>/', views.payment_view, name='payment'),
]

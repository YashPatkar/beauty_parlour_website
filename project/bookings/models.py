"""
Bookings app - Appointment, Cart, CartItem, UserFavourite.
User books Appointment for a Service; Cart and Favourites for users (not admins).
"""
from django.db import models
from django.conf import settings


class Cart(models.Model):
    """One cart per user; holds CartItems for add-to-cart."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.service.price * item.quantity for item in self.items.select_related('service'))

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """A service in the user's cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'service']]

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"


class UserFavourite(models.Model):
    """Saved service for quick book later (favourites)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourite_services'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'service']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.service.name}"


class Appointment(models.Model):
    """Appointment booked by a user for a service."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    staff = models.ForeignKey(
        'services.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.service.name} on {self.date}"

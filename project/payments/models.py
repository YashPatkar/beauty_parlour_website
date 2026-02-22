"""
Payments app - demo/simulated payment only.
Payment per Appointment; SavedPaymentMethod for profile (demo cards).
"""
from django.db import models
from django.conf import settings


class SavedPaymentMethod(models.Model):
    """Demo saved card - last 4 digits, type, nickname. No real card data."""
    CARD_TYPE = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('rupay', 'RuPay'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_payment_methods'
    )
    last_four = models.CharField(max_length=4)  # Last 4 digits only
    card_type = models.CharField(max_length=20, choices=CARD_TYPE)
    nickname = models.CharField(max_length=50, blank=True)  # e.g. "My Visa"
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"****{self.last_four} ({self.get_card_type_display()})"


class Payment(models.Model):
    """Payment record for an appointment - simulated gateway."""
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    appointment = models.OneToOneField(
        'bookings.Appointment',
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)  # Demo: pay_xxx format for Razorpay-like
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.amount} ({self.status})"

"""
Services app models: Service, Staff, Feedback, Contact.
"""
from django.db import models


class Service(models.Model):
    """Beauty service offered by the parlour."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=60, help_text='Approx duration in minutes')
    image_url = models.URLField(blank=True, help_text='Optional image URL for service card')
    location = models.CharField(max_length=100, blank=True, help_text='Branch or area e.g. Chembur, Bandra')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Staff(models.Model):
    """Staff member who can be assigned to appointments."""
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, help_text='Optional photo URL')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Staff'

    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Customer feedback - linked to User."""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.user.username} - {self.rating} stars"


class Contact(models.Model):
    """Contact form submission - stores name, email, message."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name}"

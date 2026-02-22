"""
Accounts app - User (Django built-in) + Profile for avatar and extra details.
"""
from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Extended user profile: avatar, phone. One-to-one with User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

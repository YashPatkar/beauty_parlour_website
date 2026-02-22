from django.contrib import admin
from .models import Payment, SavedPaymentMethod


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'method', 'status', 'transaction_id')
    list_filter = ('status', 'method')


@admin.register(SavedPaymentMethod)
class SavedPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_four', 'card_type', 'nickname', 'is_default')
    list_filter = ('card_type',)

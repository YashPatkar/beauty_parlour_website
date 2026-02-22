"""
Payments app - Simulated payment only.
User selects Cash/Card/Online; for Online we simulate success/failure.
On success: Payment status=Paid, generate demo transaction_id, redirect to My Appointments.
"""
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookings.models import Appointment
from .models import Payment


def _generate_demo_transaction_id():
    """Generate Razorpay-style demo transaction ID (pay_xxxxxxxxxxxx)."""
    return 'pay_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=14))


@login_required
def payment_view(request, appointment_id):
    """Razorpay-style payment page: Cards, UPI, Netbanking (demo). Saves pay_xxx transaction ID."""
    appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)
    if appointment.status == 'cancelled':
        messages.error(request, 'This appointment is cancelled.')
        return redirect('my_appointments')

    if hasattr(appointment, 'payment') and appointment.payment.status == 'paid':
        messages.info(request, 'This appointment is already paid.')
        return redirect('my_appointments')

    amount = appointment.service.price
    from .models import SavedPaymentMethod
    saved_methods = SavedPaymentMethod.objects.filter(user=request.user)

    if request.method == 'POST':
        pay_mode = request.POST.get('pay_mode')  # razorpay (card/upi/netbanking) or salon (cash)
        if pay_mode == 'salon':
            # Pay at salon (cash/card at counter) - no gateway
            payment, created = Payment.objects.get_or_create(
                appointment=appointment,
                defaults={'amount': amount, 'method': 'cash', 'status': 'pending'}
            )
            payment.amount = amount
            payment.method = 'cash'
            payment.status = 'paid'
            payment.transaction_id = _generate_demo_transaction_id()
            payment.save()
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, f'Payment recorded. Transaction ID: {payment.transaction_id}')
            return redirect('my_appointments')
        # Razorpay-style online payment (demo)
        payment, created = Payment.objects.get_or_create(
            appointment=appointment,
            defaults={'amount': amount, 'method': 'online', 'status': 'pending'}
        )
        payment.amount = amount
        payment.method = 'online'
        payment.save()
        simulate_success = request.POST.get('simulate_success', '1') == '1'
        if simulate_success:
            payment.status = 'paid'
            payment.transaction_id = _generate_demo_transaction_id()
            payment.save()
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, f'Payment successful! Transaction ID: {payment.transaction_id}')
            return redirect('my_appointments')
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(request, 'Payment failed (simulated). Try again.')
            return render(request, 'payments/payment.html', {
                'appointment': appointment,
                'amount': amount,
                'saved_methods': saved_methods,
            })

    return render(request, 'payments/payment.html', {
        'appointment': appointment,
        'amount': amount,
        'saved_methods': saved_methods,
    })

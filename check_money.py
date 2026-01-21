import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')
django.setup()
from hotel.models import Booking, Payment
from django.db.models import Sum

print(f"Total Bookings: {Booking.objects.count()}")
print(f"Total Payments: {Payment.objects.count()}")
print(f"Total Revenue Sum: {Payment.objects.aggregate(Sum('amount'))}")
for p in Payment.objects.all()[:5]:
    print(f"Payment: {p.amount} (Method: {p.payment_method})")

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')
django.setup()
from hotel.models import Booking

b = Booking.objects.first()
if b:
    print(f"Guest: {b.guest_name}")
    print(f"Room: {b.room.number} (Price: {b.room.price_per_night})")
    print(f"Check In: {b.check_in_date}")
    print(f"Check Out: {b.check_out_date}")
    days = (b.check_out_date - b.check_in_date).days
    print(f"Calculated Days: {days}")
    print(f"Expected Amount: {days * b.room.price_per_night}")

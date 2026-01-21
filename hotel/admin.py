from django.contrib import admin
from .models import Room, Booking, Payment, Review

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)

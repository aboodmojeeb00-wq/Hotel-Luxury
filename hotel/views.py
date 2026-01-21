from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Room, Booking, Payment, Review
from .forms import RoomForm, BookingForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    return render(request, 'hotel/home.html')

def dashboard(request):
    if not request.user.is_staff:
        return redirect('room_list')

    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(is_occupied=True).count()
    available_rooms = total_rooms - occupied_rooms
    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    total_reviews = Review.objects.count()
    total_payments = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'recent_bookings': recent_bookings,
        'total_reviews': total_reviews,
        'total_payments': total_payments,
    }
    return render(request, 'hotel/dashboard.html', context)

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'hotel/room_detail.html', {'room': room})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room created successfully.")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'hotel/room_form.html', {'form': form, 'title': 'Add Room'})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully.")
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotel/room_form.html', {'form': form, 'title': 'Edit Room'})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted.")
        return redirect('room_list')
    return render(request, 'hotel/room_confirm_delete.html', {'room': room})



@login_required(login_url='login')
def booking_list(request):
    if request.user.is_staff:
        
        bookings = Booking.objects.all().order_by('-created_at')
    else:
      
        messages.error(request, "Access restricted to Admins.")
        return redirect('room_list')
        
    return render(request, 'hotel/booking_list.html', {'bookings': bookings})

@login_required(login_url='login')
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
   
    if not request.user.is_staff:
         messages.error(request, "Access denied.")
         return redirect('room_list')
         
    return render(request, 'hotel/booking_detail.html', {'booking': booking})


@login_required(login_url='login')
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            room_obj = form.cleaned_data.get('room')
            if room_obj.is_occupied:
                messages.error(request, "Error: This room is already reserved/occupied.")
                return render(request, 'hotel/booking_form.html', {'form': form, 'title': 'Add Booking'})

            booking = form.save(commit=False)
          
            booking.save()
            
            check_in = booking.check_in_date
            check_out = booking.check_out_date
            try:
                days = (check_out - check_in).days
            except:
                days = 1
            if days < 1: days = 1
            
            per_night = booking.room.price_per_night
            total_amount = days * per_night
            method = form.cleaned_data.get('payment_method')

            Payment.objects.create(
                booking=booking,
                amount=total_amount,
                payment_method=method
            )

            room = booking.room
            if not room.is_occupied:
                room.is_occupied = True
                room.save()
            
            messages.success(request, f"Booking Successful! Total: {total_amount}")
          
            if request.user.is_staff:
                return redirect('booking_list')
            else:
                return redirect('room_list')
    else:
        form = BookingForm()
    return render(request, 'hotel/booking_form.html', {'form': form, 'title': 'Add Booking'})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            
           
            check_in = booking.check_in_date
            check_out = booking.check_out_date
            try:
                days = (check_out - check_in).days
            except:
                days = 1
            if days < 1: days = 1
            
            new_amount = days * booking.room.price_per_night
            
            payment = booking.payment_set.first()
            if payment:
                payment.amount = new_amount
                payment.save()
            
            booking.room.is_occupied = True
            booking.room.save()
            messages.success(request, "Booking updated.")
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'hotel/booking_form.html', {'form': form, 'title': 'Edit Booking'})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        room = booking.room
        booking.delete()
        if not Booking.objects.filter(room=room).exists():
            room.is_occupied = False
            room.save()
            messages.info(request, f"Booking cancelled. Room {room.number} is now AVAILABLE.")
        else:
             messages.info(request, "Booking cancelled.")
        return redirect('booking_list')
    return render(request, 'hotel/booking_confirm_delete.html', {'booking': booking})



@login_required(login_url='login')
def payment_list(request):
    if not request.user.is_staff:
        messages.error(request, "Access Restricted.")
        return redirect('room_list')
        
    payments = Payment.objects.all().order_by('-date')
    return render(request, 'hotel/payment_list.html', {'payments': payments})

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'hotel/review_list.html', {'reviews': reviews})

@login_required(login_url='login')
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'hotel/review_form.html', {'form': form, 'title': 'Write a Review'})

@login_required(login_url='login')
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user or request.user.is_staff:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Review updated.")
                return redirect('review_list')
        else:
            form = ReviewForm(instance=review)
        return render(request, 'hotel/review_form.html', {'form': form, 'title': 'Edit Review'})
    else:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('review_list')

@login_required(login_url='login')
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user or request.user.is_staff:
        if request.method == 'POST':
            review.delete()
            messages.success(request, "Review deleted.")
            return redirect('review_list')
        return render(request, 'hotel/review_confirm_delete.html', {'review': review})
    else:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect('review_list')


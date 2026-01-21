from django import forms
from .models import Room, Booking, Review
from django.db.models import Q

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'price_per_night', 'capacity', 'description', 'is_occupied', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('NETWORK', 'Network'),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS, required=True, label="Payment Method")

    class Meta:
        model = Booking
        fields = ['guest_name', 'room', 'check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
       
        if self.instance and self.instance.pk:
            
             self.fields['room'].queryset = Room.objects.filter(Q(is_occupied=False) | Q(pk=self.instance.room.pk))
        else:
             self.fields['room'].queryset = Room.objects.filter(is_occupied=False)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['room', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
        }

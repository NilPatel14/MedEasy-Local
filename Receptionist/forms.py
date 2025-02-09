from django import forms
from authorization.models import User
from django.core.exceptions import ValidationError
from .models import *

class BookingForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=User.objects.filter(is_patient=True),
        widget=forms.Select(attrs={
            'placeholder': 'Select Patient',
            'class': 'form-control'
        })
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(attrs={
            
            'placeholder': 'Select Room',
            'class': 'form-control'
        })
    )
    bed = forms.ModelChoiceField(
        queryset=Bed.objects.all(),
        widget=forms.Select(attrs={
            'placeholder': 'Select Bed',
            'class': 'form-control'
        })
    )
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={

            'class': 'form-control',
            'type': 'date'
        })
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['id']

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')
        bed = cleaned_data.get('bed')

        if check_in and check_out and room and bed:
            existing_booking = Booking.objects.filter(
                room=room,
                bed=bed,
                check_in__lte=check_out,  # Overlapping condition
                check_out__gte=check_in  # Overlapping condition
            )

            if self.instance.pk:
                existing_booking = existing_booking.exclude(pk=self.instance.pk)  # Exclude the current booking if updating

            if existing_booking.exists():
                self.add_error('check_in', "This bed in the selected room is already booked for the given dates.")
                
        return cleaned_data

from django import forms
from Patient.models import Appointment

class Appointment_Booking_Form(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control large-textbox',
                'placeholder': "Enter name",
            }
        )
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Define the input format
            attrs={
                'class': 'form-control datepicker',  # Add the datepicker class
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder text
            }
        )
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Define the input format
            attrs={
                'class': 'form-control datepicker',  # Add the datepicker class
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder text
            }
        )
    )
    
    class Meta:
        model = Appointment
        fields = ['name', 'dob', 'gender', 'address', 'city', 'state', 'pincode', 'department', 'symptoms', 'preferred_date', 'preferred_time']

from django import forms
from Patient.models import Appointment





GENDER_LIST = (
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
)
# Editing date input
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class Appointment_Booking_Form(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Enter name",
                'required': True,
                'autofocus': True,
                'id' : 'name',
            }
        )
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            # format='%Y-%m-%d',  # Define the input format
            attrs={
                'class': 'form-control datepicker large-textbox',  # Add the datepicker class
                # 'placeholder': 'YYYY-MM-DD',  # Optional placeholder text
                'type' : 'date'
            }
        )
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Define the input format
            attrs={
                'class': 'form-control datepicker large-textbox',  # Add the datepicker class
                # 'placeholder': 'YYYY-MM-DD',  # Optional placeholder text
                'type' : 'date'
            }
        )
    )
    gender = forms.CharField(
        widget=forms.RadioSelect(
            choices=GENDER_LIST,
            attrs={
                'class': 'form-check-inline',
                'type' : 'radio'

            }
        )
    )
    class Meta:
        model = Appointment
        fields = ['name', 'dob', 'gender', 'address', 'city', 'state', 'pincode', 'department', 'symptoms', 'preferred_date', 'preferred_time']

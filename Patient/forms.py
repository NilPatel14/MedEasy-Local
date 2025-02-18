from django import forms
from Patient.models import *





GENDER_LIST = (
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
)
# Editing date inputra
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class Appointment_Booking_Form(forms.ModelForm):

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data['preferred_date']
        if Appointment.objects.filter(user=self.instance.user, preferred_date=preferred_date).exists():
            raise forms.ValidationError("You already have an appointment on this date.")
        return preferred_date
    
    
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
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': "Enter address",
                'rows': 5,
                'cols': 20,

            }
        )
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Enter city",

            }
        )
    )

    state = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter state',
            }
        )
    )
    pincode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Enter pincode",
            }
        )
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': "Select department"
            }
        )
    )

    symptoms = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': "Enter symptoms",
                'rows' : 5
                }
        )
    )

    preferred_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control',
                'type' : 'time',
                'placeholder' : 'Enter preferred time',
                }
        )
    )
    class Meta:
        model = Appointment
        fields = ['name', 'dob', 'gender', 'address', 'city', 'state', 'pincode', 'department', 'symptoms', 'preferred_date', 'preferred_time']

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    otp = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter OTP'
        }),
        help_text="OTP will be sent to your email."
    )
    adhhar_no = forms.CharField(
        required=False, 
        
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Aadhaar number',
            'style': 'overflow: hidden;'
        })
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'otp', 'phone_no', 'adhhar_no',]

class EditAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'dob', 'gender', 'address', 'city', 'state', 'pincode', 'department', 'symptoms',]
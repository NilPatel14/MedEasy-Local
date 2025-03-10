import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import ContactModel, User

class Contact_Form(forms.ModelForm):
    contact_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    contact_subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter subject'
        })
    )
    contact_dis = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter description',
            'rows': 3
        })
    )

    class Meta:
        model = ContactModel
        exclude = ['contact_id']  # Exclude non-editable fields

    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValidationError("Please enter a valid email address.")
        return email


class User_Form(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class registrationForm(UserCreationForm):
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
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'otp', 'phone_no', 'adhhar_no', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_adhhar_no(self):
        adhhar_no = self.cleaned_data.get('adhhar_no')
        if adhhar_no and (len(adhhar_no) != 12 or not adhhar_no.isdigit()):
            raise ValidationError("Aadhaar number must be exactly 12 digits.")
        return adhhar_no

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if phone_no:
            phone_no = ''.join(re.findall(r'\d', phone_no))  # Keep only digits
            if len(phone_no) != 10 or not re.match(r'^[6-9]\d{9}$', phone_no):
                raise ValidationError("Enter a valid phone number starting with 6, 7, 8, or 9.")
        return phone_no

class Forget_Password(SetPasswordForm):
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
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    class Meta:
        model = User
        fields = ['email', 'otp', 'new_password1', 'new_password2']
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':"Enter new password"}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':"Confirm new password"}),
        }

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email

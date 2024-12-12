from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class Contact_Form(forms.ModelForm):
    contact_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Enter your name' 
    }))
    contact_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Enter your email'
    }))
    contact_subject = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Enter subject' 
    }))
    contact_dis = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder': 'Enter discription',
        'rows': 3
    }))
    class Meta:
        fields = [field.name for field in ContactModel._meta.fields if field.name != 'contact_id']
        model = ContactModel

class User_Form(forms.ModelForm):
    class Meta:
        model = UserModel  # Use your custom UserModel here
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }),
        }

class registrationForm(forms.ModelForm):
    class Meta:
        model = UserModel  # Use your custom UserModel here
        fields = "__all__"
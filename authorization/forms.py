from django import forms
from .models import *


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
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control' ,
        
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control' ,

    }))

    class Meta:
        fields = [field.name for field in ContactModel._meta.fields if field.name != 'user_id']
        models = UserModel
        
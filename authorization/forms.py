from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm


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

class User_Form(forms.Form ):
    # class Meta:
    #     model = User  # Use your custom UserModel here
    #     fields = ['username', 'password']
    #     widgets = {
    #         'username': forms.TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter your username',
    #         }),
    #         'password': forms.PasswordInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter your password',
    #         }),
    #     }

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter password'
            }
        )
    )

class registrationForm(UserCreationForm):
    
    
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter username'
            }
        )
    )

    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter first name'
            }
        )
    )
    last_name = forms.CharField(
        label="Last name",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter last name'
            }
        )
    )

    phone_no = forms.CharField(
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter phone number'
            }
        )
    )



    email = forms.EmailField(
        label="Email",
        max_length=200, help_text='Required. 150 or fewer',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Enter email',
                                 'required': True
                                 }))
    gender = forms.CharField(
        label="Gender",
        max_length=20,
        widget=forms.RadioSelect(
            attrs={
                'class' : 'form-check-input',
                # 'placeholder' : 'Select gender'
            },
            choices=(('male','male'),('female','female'),)
        )
    )

    password1 = forms.CharField(
        label="Password",
        max_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter password'
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        max_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter confirm password'
            }
        )
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_no','gender','password1','password2']        

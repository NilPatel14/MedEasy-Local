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

# class registrationForm(UserCreationForm):
    
    
#     username = forms.CharField(
#         label="Username",
#         widget=forms.TextInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter username'
#             }
#         )
#     )

#     first_name = forms.CharField(
#         label="First name",
#         widget=forms.TextInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter first name'
#             }
#         )
#     )
#     last_name = forms.CharField(
#         label="Last name",
#         widget=forms.TextInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter last name'
#             }
#         )
#     )

#     phone_no = forms.CharField(
#         label="Phone number",
#         widget=forms.TextInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter phone number'
#             }
#         )
#     )



#     email = forms.EmailField(
#         label="Email",
#         max_length=200, help_text='Required. 150 or fewer',
#                              widget=forms.EmailInput(attrs={
#                                  'class': 'form-control',
#                                  'placeholder': 'Enter email',
#                                  'required': True
#                                  }))
#     gender = forms.CharField(
#         label="Gender",
#         max_length=20,
#         widget=forms.RadioSelect(
#             attrs={
#                 'class' : 'form-check-input',
#                 # 'placeholder' : 'Select gender'
#             },
#             choices=(('male','male'),('female','female'),)
#         )
#     )

#     password1 = forms.CharField(
#         label="Password",
#         max_length=8,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter password'
#             }
#         )
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         max_length=8,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class' : 'form-control',
#                 'placeholder' : 'Enter confirm password'
#             }
#         )
#     )

    
#     usertype = forms.CharField(widget=forms.Select(
#         attrs={'class': 'form-control'},
#     ))
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','email','phone_no','usertype','password1','password2']        


class registrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }
        )
    )

    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }
        )
    )

    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }
        )
    )

    phone_no = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }
        )
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }
        )
    )

    otp = forms.CharField(
        label='Enter OTP',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder':'Enter otp'
            }
        ),
        help_text="OTP will be sent to your EMAIL"
    )

    adhhar_no = forms.CharField(
        label="Adhhar Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter adhhar number',
                'style': 'overflow: hidden;'
                }
        )
    )
  

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','otp', 'phone_no','adhhar_no', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Add any specific email validation you need here
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                raise ValidationError("Please enter a valid email address.")
        return email

    def clean_adhhar_no(self):
        adhhar_no = self.cleaned_data.get('adhhar_no')
        if adhhar_no:
            # Ensure that the Aadhaar number is exactly 12 digits
            if len(adhhar_no) != 12 or not adhhar_no.isdigit():
                  raise ValidationError("Aadhaar number must be exactly 12 digits.")
        return adhhar_no        
    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if phone_no:
            # Remove any non-digit characters (if user accidentally enters symbols or spaces)
            phone_no = ''.join(re.findall(r'\d', phone_no))
            
            # Check if phone number is exactly 10 digits
            if len(phone_no) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")
            
            # Optionally check for a valid phone number format (e.g., starts with a valid prefix)
            # This step can be customized depending on the country's phone number format
            if not re.match(r'^[6-9]\d{9}$', phone_no):
                raise ValidationError("Enter a valid phone number starting with 6, 7, 8, or 9.")
        
        return phone_no
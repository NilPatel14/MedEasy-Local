from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *

from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import User_Form, Contact_Form
import random
from django.http import HttpResponse,FileResponse
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.timezone import now



def _redirect_by_role(user):
    usertype = str(user.usertype) if user.usertype else ""
    if usertype == 'Doctor':
        return redirect("/doctor/profile/")
    elif usertype == 'Patient':
        return redirect("/patient/profile/")
    elif usertype == 'Admin' or user.is_superuser:
        return redirect("/secure-admin/")
    elif usertype == 'receptionist':
        return redirect("/receptionist/profile/")
    return None


def home(request):
    if request.user.is_authenticated:
        r = _redirect_by_role(request.user)
        if r:
            return r
    if request.method == "POST":
        
        contactForm = Contact_Form(request.POST)
        if contactForm.is_valid():
            contactForm.save()
            messages.success(request, "Your message has been sent successfully.")
            contactForm = Contact_Form()
        else:
            messages.error(request, "Enter valid data")
    else:
        contactForm = Contact_Form()
    receptionist_type = usertypeModel.objects.get(usertype="receptionist")  
    receptionist_count = User.objects.filter(usertype=receptionist_type).count()
    dept=Department.objects.all().count()
    d1_type=usertypeModel.objects.get(usertype="Doctor")
    d1_count=User.objects.filter(usertype=d1_type).count()  
    return render(request, "Home/home.html", {"contactForm": contactForm,'receptionist_count':receptionist_count,'dept':dept,'d1_count':d1_count})




def log_in_page(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user) or redirect("/")

    if request.method == "POST":
        form = User_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                user.last_login = now()
                user.save()
                login(request, user)
                return _redirect_by_role(user) or redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = User_Form()

    return render(request, "Home/login.html", {'login_form': form})


def log_out(request):
    logout(request)
    # messages.success(request, "Logged out successfully.")
    return redirect("authorization:log_in")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {'user': request.user})
    else:
        return redirect("authorization:log_in")




# Send otp and varify email
def generate_otp():
    return random.randint(100000, 999999)

import json
from django.http import JsonResponse

def send_otp_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid request data"})

        email = data.get('email', '').strip()
        if not email:
            return JsonResponse({"status": "error", "message": "Email not provided"})

        otp = random.randint(100000, 999999)
        request.session['otp'] = otp

        try:
            send_mail(
                "Your OTP Code - MedEasy",
                f"Your OTP for MedEasy registration is: {otp}\n\nThis OTP is valid for this session only.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({"status": "success", "message": "OTP sent!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Failed to send email: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid request"})



def verify_otp(request):
    if request.method == "POST":
        
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if entered_otp == str(session_otp):
            return True
        else:
            return False
    return render(request,'Home/registration.html')



def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = registrationForm(request.POST)
            if form.is_valid():
                otp_entered = request.POST.get('otp', '').strip()
                session_otp = str(request.session.get('otp', ''))

                if not session_otp:
                    messages.error(request, "OTP not sent yet. Please click 'Verify Email' first.")
                elif otp_entered != session_otp:
                    messages.error(request, "Invalid OTP. Please enter the correct OTP sent to your email.")
                else:
                    try:
                        patient_usertype = usertypeModel.objects.get(usertype="Patient")
                        user = form.save(commit=False)
                        user.usertype = patient_usertype
                        user.is_patient = True
                        user.full_clean()
                        user.save()
                        request.session.pop('otp', None)
                        messages.success(request, "Account created successfully! Please login.")
                        return redirect("authorization:log_in")
                    except usertypeModel.DoesNotExist:
                        messages.error(request, "Registration error. Please contact support.")
                    except Exception as e:
                        messages.error(request, f"Error: {str(e)}")
            # field-level errors are shown inline — no additional generic message needed
        else:
            form = registrationForm()

        return render(request, "Home/registration.html", {"form": form})
    else:
        return _redirect_by_role(request.user) or redirect("/")

# def forget_password(request):
#     if request.method == "POST":
#         form = Forget_Password(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             email_entered = request.POST.get('email', None)
#             print(email_entered)
#             otp = request.POST.get('otp')  # Assuming the OTP is entered by the user
#             if email_entered:
                        
#                 if User.objects.filter(email=email_entered).exists():
#                     if verify_otp(request):  # Pass the OTP directly
#                         form.save()
#                         messages.success(request, "Password changed successfully!")
#                     else:
#                         send_otp_email(form.cleaned_data['email'])
#                         messages.error(request, "Something is wrong with the data!")
#                 else:
#                     messages.error(request, "Enter a valid email")
#     else:
#         form = Forget_Password(None)

#     template = 'Home/ForgetPassword.html'
#     return render(request, template, {'form': form})
    
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'Home/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('authorization:password_reset_done')

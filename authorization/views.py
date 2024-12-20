from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import User_Form, Contact_Form
import random
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse



def home(request):
    if request.method == "POST":
        contactForm = Contact_Form(request.POST)
        if contactForm.is_valid():
            contactForm.save()
            messages.success(request, "Your message has been sent successfully.")
        else:
            messages.error(request, "Enter valid data")
    else:
        contactForm = Contact_Form()
    return render(request, "home.html", {"contactForm": contactForm})




def log_in_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = User_Form(request.POST)
            msg = None
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect("profile")
                else:
                    print('something went wrong')
                    messages.error(request, "Invalid username or password.")
            else:
                # If form is not valid, messages will be handled automatically by the template
                messages.error(request, "Please fix the errors below.")
        else:
            form = User_Form()
        
        return render(request, "login.html", {'login_form': form})
    else:
        return redirect("profile")


def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("log_in")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {'user': request.user})
    else:
        return redirect("log_in")




# Send otp and varify email
def generate_otp():
    return random.randint(100000, 999999)



# def send_otp_email(request):
        
   # Get the email from the form data
    # if request.method == 'POST':
        # email = request.POST.get('email')
        # email= 'deepdave3205@gmail.com'
        
    #     otp = generate_otp()  # Generate OTP

    #     # Save OTP in session or a temporary model (using session for this example)
    #     request.session['otp'] = otp

    #     # Send OTP to user's email
    #     subject = 'Your OTP for Email Verification'
    #     message = f'Your OTP for email verification is: {otp}'
    #     from_email = settings.DEFAULT_FROM_EMAIL  # or provide your email here
        
    #     send_mail(subject, message, from_email, [email])

    #     # Provide feedback to the user
    #     messages.success(request, 'OTP sent to your email address.')
    #     return redirect('registrationurl')
    # # else:
    # #     # email = request.GET.get('email')
    # #     print(email,"From get")
    # #     return redirect('registrationurl')
import json
from django.http import JsonResponse

def send_otp_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON data
            email = data.get('email')  # Extract email from JSON
            
            if not email:
                return JsonResponse({"status": "error", "message": "Email not provided"})
            
            # Proceed with OTP logic...
            print(f"Received email: {email}")  # Print to verify

            # Your OTP sending logic here
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            send_mail(
                "Your OTP Code",
                f"Your OTP is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return JsonResponse({"status": "success", "message": "OTP sent!"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"})

    return JsonResponse({"status": "error", "message": "Invalid request"})



def verify_otp(request):
    if request.method == "POST":
        
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if entered_otp == str(session_otp):
            return True
        else:
            return False
    return render(request,'registration.html')

# ===========   Registration    ==============
# def register(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = registrationForm(request.POST or None)
#             if form.is_valid():
#                 form.save()
#                 email_entered = request.POST.get('email',None)
#                 print(email_entered)
#                 # Create user object without committing to the database
#                 otp = str(form.cleaned_data['email'])
#                 if (verify_otp(otp)):
#                     user = form.save(commit=False)

                    
#                     # Assign default user type and roles (example: Patient)
#                     try:
#                         # Fetch the 'Patient' usertype instance from usertypeModel
#                         patient_usertype = usertypeModel.objects.get(usertype="Patient")
#                         user.usertype = patient_usertype
#                         user.is_patient = True

#                         # Validate before saving
#                         user.full_clean()
#                         user.save()
    
#                         messages.success(request, "User created successfully!")
#                         return redirect("log_in")
#                     except usertypeModel.DoesNotExist:
#                         messages.error(request, "The specified usertype 'Patient' does not exist.")
#                     except Exception as e:
#                         messages.error(request, f"Error: {str(e)}")
#                 else:
#                     send_otp_email(form.cleaned_data['email'])
#                     messages.error(request, "Something is wrong with the data!")
#             else:
#                 messages.error(request,"Enter valid OPT")
#         else:
#             form = registrationForm()

#         return render(request, "registration.html", {"form": form})
#     else:
#         return redirect("profile")



def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = registrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                email_entered = request.POST.get('email', None)
                print(email_entered)

                # Extract OTP from the form or somewhere else
                otp = request.POST.get('otp')  # Assuming the OTP is entered by the user

                if verify_otp(request):  # Pass the OTP directly
                    user = form.save(commit=False)

                    # Assign default user type and roles (example: Patient)
                    try:
                        # Fetch the 'Patient' usertype instance from usertypeModel
                        patient_usertype = usertypeModel.objects.get(usertype="Patient")
                        user.usertype = patient_usertype
                        user.is_patient = True

                        # Validate before saving
                        user.full_clean()
                        user.save()

                        messages.success(request, "User created successfully!")
                        return redirect("log_in")
                    except usertypeModel.DoesNotExist:
                        messages.error(request, "The specified usertype 'Patient' does not exist.")
                    except Exception as e:
                        messages.error(request, f"Error: {str(e)}")
                else:
                    send_otp_email(form.cleaned_data['email'])
                    messages.error(request, "Something is wrong with the data!")
            else:
                messages.error(request, "Enter a valid OTP")
        else:
            form = registrationForm()

        return render(request, "registration.html", {"form": form})
    else:
        return redirect("profile")

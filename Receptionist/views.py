from django.shortcuts import render,redirect
from django.conf import settings
from django.apps import apps
from Doctor.models import Appointment,Prescription
# from django.http import JsonResponse
# from .models import PatientRecord
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from authorization.models import usertypeModel
from authorization.forms import registrationForm
from authorization.views import verify_otp, send_otp_email
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import BookingForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Bed, Room, Booking
from django.contrib import messages
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name
        template = "Receptionist/index.html"
        return render(request,template,{'name':name})
    else:
        return redirect('authorization:log_in')
    
def dashboard(request):    
    if request.user.is_authenticated:
        # Query all appointments
        appointments = Appointment.objects.all()
        
        # Create a list to store appointment data along with department users
        appointment_data = []
        
        for appointment in appointments:
            # Get department related to this appointment
            department = appointment.department  # Assuming department is a ForeignKey or related field
            
            # Fetch all users linked to this department
            # Assuming AUTH_USER_MODEL has a 'department' field
            UserModel = apps.get_model(settings.AUTH_USER_MODEL)
            users_in_department = UserModel.objects.filter(department=department)
            # status = appointment.status

            # Append appointment and department user details to the list
            appointment_data.append({
                'appointment': appointment,
                'users_in_department': users_in_department,
            })
        
        # Pass the structured data to the template
        template="Receptionist/Dashboard.html"
        return render(request, template, {'appointment_data': appointment_data})
    else:
        # If user is not authenticated, redirect to login
        return redirect('authorization:log_in')

# Add new patient record
def AddPatientRecord(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
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

                        # messages.success(request, "User created successfully!")
                        return redirect("authorization:log_in")
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

        return render(request, "Receptionist/AddPatient.html", {"form": form})
    else:
        return redirect("Doctor:index")

def OPD(request):
    if request.user.is_authenticated:
        # UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        # dep = request.user.department_id
        # users_in_department = UserModel.objects.filter(department=department)
        # Use filter to get a queryset of all appointments for the department with id 1
        today = date.today()
        print(today)
        appointments = Appointment.objects.all()
        pre = Prescription.objects.all()
        opd = pre.filter(ipd_opd="OPD")
        ipd = pre.filter(ipd_opd="IPD")
        template="Receptionist/OPD.html"
        return render(request, template, {'data': appointments,'pre':pre,'ipd':ipd,'opd':opd,'today':today})

    else:
        return redirect('authorization:log_in')
    
def IPD(request):
    if request.user.is_authenticated:
        # UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        # dep = request.user.department_id
        # users_in_department = UserModel.objects.filter(department=department)
        # Use filter to get a queryset of all appointments for the department with id 1
        today = date.today()
        appointments = Appointment.objects.all()    
        pre = Prescription.objects.all()
        opd = pre.filter(ipd_opd="OPD")
        ipd = pre.filter(ipd_opd="IPD")
        template="Receptionist/IPD.html"
        return render(request, template, {'data': appointments,'pre':pre,'ipd':ipd,'opd':opd,'today':today})

    else:
        return redirect('authorization:log_in')



def generate_otp():
    return random.randint(100000, 999999)

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
    return render(request,'Receptionist/AddPatient.html')


def room_details(request):
    if request.user.is_authenticated:
        all_booking = Booking.objects.all()
        
        # Check and update availability of rooms where check_out date has passed
        for booking in all_booking:
            if booking.check_out and booking.check_out < date.today() and not booking.room.availability:
                booking.room.availability = True
                booking.room.save()

        template = "Receptionist/roomdetails.html"
        return render(request, template, {'all_booking': all_booking})
    else:
        return redirect('authorization:log_in')
    
def room(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                # Get cleaned data from the form
                check_in = form.cleaned_data['check_in']
                check_out = form.cleaned_data['check_out']
                
                # Check if check_in date is in the past
                if check_in < date.today():
                    messages.error(request, 'Check-in date cannot be in the past.')
                    return render(request, "Receptionist/room.html", {'form': form})

                # Check if check_out date is before check_in date
                if check_out < check_in:
                    messages.error(request, 'Check-out date cannot be before check-in date.')
                    return render(request, "Receptionist/room.html", {'form': form})

                # Save the booking if the dates are valid
                booking = form.save()

                # Update room availability if necessary
                if form.cleaned_data['room'].availability == True:
                    form.cleaned_data['room'].availability = False
                    form.cleaned_data['room'].save()

                messages.success(request, 'Booking successful')
                return redirect('Receptionist:room_details')
            else:
                messages.error(request, 'Booking failed! Please check the dates or room selection.')
        else:
            form = BookingForm()

        template = "Receptionist/room.html"
        return render(request, template, {'form': form})
    else:
        return redirect('authorization:log_in')

import logging

logger = logging.getLogger(__name__)

def get_beds(request):
    room_id = request.GET.get('room_id')

    if not room_id:
        return JsonResponse({'error': 'Room ID is required'}, status=400)

    try:
        beds = Bed.objects.filter(room_id=room_id).values('id', 'bed_no')  # Use 'bed_no' instead of 'bed_number'
        return JsonResponse(list(beds), safe=False)
    except Exception as e:
        logger.error(f"Error in get_beds view: {e}")  # Log the error
        return JsonResponse({'error': str(e)}, status=500)
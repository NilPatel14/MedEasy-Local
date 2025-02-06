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


def room(request):
    template="Receptionist/room.html"
    return render(request,template)

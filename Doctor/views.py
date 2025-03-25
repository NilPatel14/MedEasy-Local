from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
import random
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from authorization.models import *
from Patient.models import *
from django.apps import apps
from datetime import datetime


# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated:
        template = "Doctor/index.html"
        user = request.user
        name = user.first_name
        return render(request,template,{'name':name})
    else:
        return redirect("authorization:log_in")
    
from datetime import datetime as dt
def dashboard_show(request):
    if request.user.is_authenticated:
        # UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        dep = request.user.department_id
        # users_in_department = UserModel.objects.filter(department=department)
        # Use filter to get a queryset of all appointments for the department with id 1
        appointments = Appointment.objects.filter(department_id=dep)
        date=str(dt.now().date())
        appointments1 = Appointment.objects.filter(preferred_date=date,department_id=dep)

        pre = Prescription.objects.filter(appointment_id__in=appointments)
        opd = pre.filter(ipd_opd="OPD")
        ipd = pre.filter(ipd_opd="IPD")
        print(date)
        print(type(date))
        template = "Doctor/dashboard.html"
        return render(request, template, {'data': appointments,'pre':pre,'ipd':ipd,'opd':opd,'date':date,'data1':appointments1})
    else:
        return redirect("authorization:log_in")
# import logging

# logger = logging.getLogger(__name__)

# def dashboard_show(request):
#     if request.user.is_authenticated:
#         try:
#             dep = request.user.department_id
#             appointments = Appointment.objects.filter(department_id=dep)
#             pre = Prescription.objects.filter(appointment_id__in=appointments)

#             # Filter prescriptions by IPD/OPD
#             opd = pre.filter(ipd_opd="OPD")
#             ipd = pre.filter(ipd_opd="IPD")

#             logger.debug("Appointments: %s", appointments)
#             logger.debug("Prescriptions: %s", pre)
#             logger.debug("OPD Prescriptions: %s", opd)
#             logger.debug("IPD Prescriptions: %s", ipd)

#             template = "Doctor/dashboard.html"
#             return render(request, template, {
#                 'data': appointments,
#                 'pre': pre,
#                 'ipd': ipd,
#                 'opd': opd
#             })
#         except Exception as e:
#             logger.error("Error fetching data: %s", e)
#             return render(request, "error.html", {"message": "Error fetching data."})
#     else:
#         return redirect("authorization:log_in")



# def prescription_show(request, id=0):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = Prescription_Form(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Prescription saved successfully.")
#             else:
#                 messages.error(request, "Enter valid data.")
#         else:
#             # Fetch appointment details to prefill the form
#             try:
#                 appointment = Appointment.objects.get(id=id)
#             except Appointment.DoesNotExist:
#                 messages.error(request, "Appointment not found.")
#                 return redirect("Doctor:dashboard")

#             # Calculate age from the date of birth
#             birth_date = appointment.dob
#             today = datetime.now().date()
#             age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

#             # Prefill the form with initial data
#             initial_data = {
#                 'patient_name': appointment.name,
#                 'patient_age': age,
#                 # Add more fields if needed
#                 'gender': appointment.gender,
#                 'problem' : appointment.symptoms,
#             }
#             form = Prescription_Form(initial=initial_data)

#         # Render the template with the form
#         template = "Doctor/prescription.html"
#         return render(request, template, {'form': form})
#     else:
#         return redirect("authorization:log_in")


from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import Prescription_Form
from .models import Appointment
import datetime

def prescription_show(request, id=1):
    if request.user.is_authenticated:
        if request.method == 'POST':
            appointment = Appointment.objects.get(id=id)
            request.POST = request.POST.copy()  # Make it mutable
            request.POST['appointment_id'] = appointment.id
            form = Prescription_Form(request.POST)
            print(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Prescription saved successfully.")
                print(request.POST)  # Check if appointment_id is included in the POST data

                return redirect('Doctor:dashboard')
            else:
                # Add errors to messages for visibility
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field}: {error}")
        else:
            # Fetch appointment details for pre-filled form data
            try:
                appointment = Appointment.objects.get(id=id)
            except Appointment.DoesNotExist:
                messages.error(request, "Appointment not found.")
                return redirect("Doctor:dashboard")

            # Pre-fill form with appointment data
            appointment.status = 'Completed'
            appointment.save()
            initial_data = {
                'patient_name': appointment.name,
                'patient_age': calculate_age(appointment.dob),
                'gender': appointment.gender,
                'problem' : appointment.symptoms,
                'appointment_id': appointment
            }
            print(initial_data)
            form = Prescription_Form(initial=initial_data)

        return render(request, 'Doctor/prescription.html', {'form': form})
    else:
        return redirect("authorization:log_in")


def calculate_age(birth_date):
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

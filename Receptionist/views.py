from django.shortcuts import render,redirect
from django.conf import settings
from django.apps import apps
from Doctor.models import Appointment,Prescription
# from django.http import JsonResponse
# from .models import PatientRecord
from django.views.decorators.csrf import csrf_exempt
from datetime import date

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

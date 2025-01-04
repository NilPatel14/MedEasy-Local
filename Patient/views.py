from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from Patient.models import *
from django.utils.timezone import datetime
from django.conf import settings
from django.apps import apps


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name
        template = "Patient/index.html"
        return render(request,template,{'name':name})
    else:
        return redirect('authorization:login')
    
from django.shortcuts import render, redirect
from django.apps import apps
from django.conf import settings
from .models import Appointment

def dashboard_show(request):
    if request.user.is_authenticated:
        # Query all appointments
        data = Appointment.objects.all()
        
        # Prepare a list to store users associated with the department
        department_users = []
        
        # Iterate through the appointments to get users associated with the department
        for i in data:
            # Fetch the department ID from the appointment
            # dept_id = 0
            dept_id = i.department  # Assuming 'department' is a ForeignKey in Appointment model
            
            # Fetch all users related to this department (assuming 'UserModel' has a foreign key to department)
            UserModel = apps.get_model(settings.AUTH_USER_MODEL)
            users_in_department = UserModel.objects.filter(department=dept_id)
            
            department_users.append(users_in_department)

        # Pass both appointment data and users associated with each department to the template
        zipped_data = zip(data, department_users)
        template = "Patient/Dashboard.html"
        return render(request, template, {'data': data, 'department_users': department_users})
    else:
        # If user is not authenticated, redirect to login
        return redirect('authorization:login')

# def dashboard_show(request):
#     if request.user.is_authenticated:
        
#     # Now you can query the model
#         data = Appointment.objects.all()
#         for i in data:
#             UserModel = apps.get_model(settings.AUTH_USER_MODEL)
#     # Now you can query the model
#             dept_id= i.department
#         # print(dept_id)
#             depart = UserModel.objects.get(department=dept_id)
#         template = "Patient/Dashboard.html"  
#         return render(request,template,{'data':data,'dep':depart})
#     else:
#         return redirect('authorization:login')
    
def bill_payment(request):
    if request.user.is_authenticated:
        template = "Patient/Payment.html"
        return render(request,template)
    else:
        return redirect('authorization:login')
    


def Book_Appointment(request):
    msg = ""
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Appointment_Booking_Form(request.POST or None)
            if form.is_valid():
                preferred_date = form.cleaned_data['preferred_date']
                # Check if the user already has an appointment on the preferred date
                existing_appointment = Appointment.objects.filter(
                    user=request.user,
                    preferred_date=preferred_date
                ).exists()

                if existing_appointment:
                    messages.error(request, "You already have an appointment on this date. Please select another date.")
                    msg = "You already have an appointment on this date please select another date"
                else:
                    # Save the appointment
                    appointment = form.save(commit=False)
                    appointment.user = request.user  # Assuming the Appointment model has a `user` field
                    appointment.save()
                    return redirect('Patient:dashboard_show')
            else:
                messages.error(request, "Something went wrong!!")

        else:
            form = Appointment_Booking_Form()

        template = "Patient/bookapp.html"
        return render(request, template, {'form': form,'error_message':msg})
    else:
        return redirect('authorization:log_in')




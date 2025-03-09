from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
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
from Doctor.models import *
from datetime import date  # ✅ Correct import


User = get_user_model()
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name
        template = "Patient/index.html"
        return render(request,template,{'name':name})
    else:
        return redirect('authorization:log_in')
    

# def dashboard_show(request):
#     if request.user.is_authenticated:
#         # Query all appointments
#         data = Appointment.objects.all()
        
#         # Prepare a list to store users associated with the department
#         department_users = []
        
#         # Iterate through the appointments to get users associated with the department
#         for i in data:
#             # Fetch the department ID from the appointment
#             # dept_id = 0
#             dept_id = i.department  # Assuming 'department' is a ForeignKey in Appointment model
            
#             # Fetch all users related to this department (assuming 'UserModel' has a foreign key to department)
#             UserModel = apps.get_model(settings.AUTH_USER_MODEL)
#             users_in_department = UserModel.objects.filter(department=dept_id)
            
#             department_users.append(users_in_department)

#         # Pass both appointment data and users associated with each department to the template
#         zipped_data = zip(data, department_users)
#         template = "Patient/Dashboard.html"
#         return render(request, template, {'data': data, 'department_users': department_users})
#     else:
#         # If user is not authenticated, redirect to login
#         return redirect('authorization:login')





def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        id = user.id
        user = get_object_or_404(User, id=id)  # Get the user instance or return 404
        
        if request.method == "POST":
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('Patient:profile')
            else:
                print(form.errors)
        else:
            form = EditProfileForm(instance=user)
        
        template = "Patient/editprofile.html"
        return render(request, template, {'form': form})
    else:
        return redirect('authorization:login')
    

def dashboard_show(request):
    if request.user.is_authenticated:
        # Get today's date
        today = date.today()
        
        # Filter appointments where preferred_date is today
        appointments = Appointment.objects.filter(user=request.user, preferred_date=today)
        appointments1 = Appointment.objects.filter(user=request.user)

        
        appointment_data1 = []

        for appointment in appointments1:
            # Update status if preferred_date is today and it's still "Pending"
            if appointment.preferred_date == today and appointment.status == "Pending":
                appointment.status = "Confirmed"  # Change as per your logic
                appointment.save()

            # Get department related to this appointment
            department = appointment.department  # Assuming department is a ForeignKey or related field
            
            # Fetch all users linked to this department
            UserModel = apps.get_model(settings.AUTH_USER_MODEL)
            users_in_department = UserModel.objects.filter(department=department)

            # Append appointment and department user details to the list
            appointment_data1.append({
                'appointment': appointment,
                'users_in_department': users_in_department,
            })
        print(appointment_data1)


        # Create a list to store appointment data along with department users
        appointment_data = []
        
        for appointment in appointments:
            # Update status if preferred_date is today and it's still "Pending"
            if appointment.preferred_date == today and appointment.status == "Pending":
                appointment.status = "Confirmed"  # Change as per your logic
                appointment.save()

            # Get department related to this appointment
            department = appointment.department  # Assuming department is a ForeignKey or related field
            
            # Fetch all users linked to this department
            UserModel = apps.get_model(settings.AUTH_USER_MODEL)
            users_in_department = UserModel.objects.filter(department=department)

            # Append appointment and department user details to the list
            appointment_data.append({
                'appointment': appointment,
                'users_in_department': users_in_department,
            })
        
        # Pass the structured data to the template
        template = "Patient/Dashboard.html"
        return render(request, template, {'appointment_data': appointment_data,'appointment_data1':appointment_data1})
    
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
        data = Appointment.objects.filter(user_id=request.user.id)
        sum = 0

        for i in data:
            print(i.department.amount)

            sum = sum + i.department.amount
            print("This is the sum")
        print(sum)
        template = "Patient/Payment.html"
        return render(request,template,{'data':sum})
    else:
        return redirect('authorization:login')
    


def Book_Appointment(request):
    msg = ""
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Appointment_Booking_Form(request.POST or None)
            if form.is_valid():
                preferred_date = form.cleaned_data['preferred_date']
                prefered_time = form.cleaned_data['preferred_time']
                # Check if the user already has an appointment on the preferred date
                existing_appointment = Appointment.objects.filter(
                    user=request.user,
                    preferred_date=preferred_date,
                    preferred_time = prefered_time
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


def check_history(request):
    if request.user.is_authenticated:
        template = "Patient/checkhistory.html"
        return render(request,template)
    else:
        return redirect('authorization:login')
    

def edit_appointment(request, id):
    if request.user.is_authenticated:
        appointment = get_object_or_404(Appointment, id=id)
        if request.method == "POST":
            form = EditAppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return redirect('Patient:dashboard_show')
            else:
                print(form.errors)
        else:
            form = EditAppointmentForm(instance=appointment)
        
        template = "Patient/editappointment.html"
        return render(request, template, {'form': form})
    else:
        return redirect('authorization:login')

def delete_appointment(request, id):
    if request.user.is_authenticated:
        appointment = get_object_or_404(Appointment, id=id)
        appointment.delete()
        return redirect('Patient:dashboard_show')
    else:
        return redirect('authorization:login')
    
def Check_Prescription_History(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
        
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
        

        prescripton = Prescription.objects.filter(appointment_id__in=appointments)
        template = "Patient/prescription.html"
        return render(request,template,{'appointment':appointment_data,'prescription':prescripton})
    else:
        return redirect('authorization:login')
    

def Check_Appointment_History(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
        
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
        

        prescripton = Prescription.objects.filter(appointment_id__in=appointments)
        template = "Patient/appointment.html"
        return render(request,template,{'appointment':appointment_data,'prescription':prescripton})
    else:
        return redirect('authorization:login')
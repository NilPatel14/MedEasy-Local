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
from Patient.models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name
        template = "Patient/index.html"
        return render(request,template,{'name':name})
    else:
        return redirect('authorization:login')
    
def dashboard_show(request):
    if request.user.is_authenticated:
        template = "Patient/Dashboard.html"
        return render(request,template)
    else:
        return redirect('authorization:login')
    
def bill_payment(request):
    if request.user.is_authenticated:
        template = "Patient/Payment.html"
        return render(request,template)
    else:
        return redirect('authorization:login')
    

from django.utils.timezone import datetime

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




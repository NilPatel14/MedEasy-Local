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
    

def Book_Appointment(request):
    if request.user.is_authenticated:
        print(f"Request method: {request.method}") 
        if request.method == "POST":
            form = Appointment_Booking_Form(request.POST or None)
            # user = Appointment.objects.all()
            # user1 = max(Appointment.objects.all())
            # print(user)
            # print(user1)
            if form.is_valid():
            
                form.save()
                return redirect('Patient:dashboard_show')
            else:
                print("Something is wrong")
                messages.error(request,"Something went wrong !!")
                return render(request, 'Patient/Book_Appointment.html', {'form': form})
        else:
            form = Appointment_Booking_Form()
        template = "Patient/bookapp.html"
        return render(request,template,{'form':form})
    else:
        return redirect('authorization:login')
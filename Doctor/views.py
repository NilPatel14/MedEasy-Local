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
    

def dashboard_show(request):
    if request.user.is_authenticated:
        template = "Doctor/dashboard.html"
        return render(request,template)
    else:
        return redirect("authorization:log_in")
    
def prescription_show(request):
    if request.user.is_authenticated:
        template = "Doctor/prescription.html"
        return render(request,template)
    else:
        return redirect("authorization:log_in")
    
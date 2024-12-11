from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.
def home(request):
    if(request.method == "POST"):
        contactForm = Contact_Form(request.POST)
        if contactForm.is_valid():
            contactForm.save()
            messages.success(request,"Your message has been sent successfully.")
        else:
            messages.error(request,"Enter valid data")
    else:
        contactForm = Contact_Form()
    return render(request,"home.html",{"contactForm" : contactForm})
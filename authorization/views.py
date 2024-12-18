# from django.shortcuts import render,redirect
# from .models import *
# from .forms import *
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.models import  User


# # Create your views here.
# def home(request):
#     if(request.method == "POST"):
#         contactForm = Contact_Form(request.POST)
#         if contactForm.is_valid():
#             contactForm.save()
#             messages.success(request,"Your message has been sent successfully.")
#         else:
#             messages.error(request,"Enter valid data")
#     else:
#         contactForm = Contact_Form()
#     return render(request,"home.html",{"contactForm" : contactForm})

# def log_in_page(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = User_Form(request.POST)
            
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 pwd = form.cleaned_data['password']
#                 data = UserModel.objects.all()
#                 for i in data:
#                     if username == i.username and pwd == i.password:
#                         # user = User(username=username,password = pwd)
#                         # login(request,user)
#                         messages.success(request, "Login successful!")
#                         return redirect("profile")  # Redirect to a relevant page
#                 else:
#                     messages.error(request, "Invalid username or password.")
#         else:
#             form = User_Form()
#         template = "login.html"
#         return render(request, template, {'login_form': form})
#     else:
#         return redirect('profile')
   

# def log_out(request):
#     logout(request)
#     return redirect("log_in")

# def profile(request):
#         template = "profile.html"
#         return render(request, template, {'user': request.user})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import User_Form, Contact_Form


def home(request):
    if request.method == "POST":
        contactForm = Contact_Form(request.POST)
        if contactForm.is_valid():
            contactForm.save()
            messages.success(request, "Your message has been sent successfully.")
        else:
            messages.error(request, "Enter valid data")
    else:
        contactForm = Contact_Form()
    return render(request, "home.html", {"contactForm": contactForm})




def log_in_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = User_Form(request.POST)
            msg = None
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect("profile")
                else:
                    print('something went wrong')
                    messages.error(request, "Invalid username or password.")
        else:
            form = User_Form()
        return render(request, "login.html", {'login_form': form})
    else:
        return redirect("profile")


def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("log_in")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {'user': request.user})
    else:
        return redirect("log_in")



# --------Registration----------
def register(request):
    print("hiii")
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = registrationForm(request.POST or None)
            if form.is_valid():
                print("User created")
                user = form.save()
                print(user)
                messages.success(request,"User created successfully...:)")
                return redirect("log_in") 
            else:
                messages.error(request,"Something is wrong with data !!")
        else:
            form = registrationForm()
        template = "registration.html"
        return render(request,template,{"form" : form})
    else:
        return redirect('profile')
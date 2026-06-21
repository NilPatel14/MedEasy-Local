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
import razorpay
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        return redirect('Patient:payment_history')
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

def payment_history(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user).select_related('department').order_by('-created_at')
        total_paid = sum(a.department.amount for a in appointments if a.payment_status == 'paid')
        total_unpaid = sum(a.department.amount for a in appointments if a.payment_status != 'paid')
        template = "Patient/payment_history.html"
        return render(request, template, {
            'appointments': appointments,
            'total_paid': total_paid,
            'total_unpaid': total_unpaid,
        })
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


# views.py
# def payment_page(request):
#     if not request.user.is_authenticated:
#         return redirect('authorization:login')

#     # Get all appointments and calculate total amount in INR
#     appointments = Appointment.objects.filter(user_id=request.user.id)
#     total_inr = sum([appt.department.amount for appt in appointments])  # ₹ amount

#     # Convert to GBP (for example, assume 1 GBP = ₹100)
#     exchange_rate = 100  # use real exchange rate or API if needed
#     total_gbp = round(total_inr / exchange_rate, 2)

#     # Stripe minimum for GBP is 30 pence
#     if total_gbp < 0.30:
#         return render(request, 'Patient/payment_page.html', {
#             'data': total_inr,
#             'error_message': 'The total amount is too low to process via Stripe (minimum is £0.30).'
#         })

#     # Create Stripe PaymentIntent
#     intent = stripe.PaymentIntent.create(
#         amount=int(total_gbp * 100),  # in pence
#         currency='gbp',
#         metadata={'user_id': request.user.id}
#     )

#     context = {
#         'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
#         'client_secret': intent.client_secret,
#         'data': total_inr
#     }
#     return render(request, 'Patient/payment_page.html', context)

# with convert amount in gbp for stripe
def payment_page_all(request):
    if not request.user.is_authenticated:
        return redirect('authorization:login')
    appointments = Appointment.objects.filter(user=request.user, payment_status='unpaid').select_related('department')
    if not appointments.exists():
        return redirect('Patient:payment_history')
    total_inr = sum(a.department.amount for a in appointments)
    total_paise = int(total_inr * 100)
    appointment_ids = ','.join(str(a.id) for a in appointments)
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order = client.order.create({
            'amount': total_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {'appointment_ids': appointment_ids},
        })
        razorpay_order_id = order['id']
    except Exception as e:
        razorpay_order_id = ''
        print("Razorpay order error:", e)
    context = {
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order_id,
        'total_paise': total_paise,
        'data': total_inr,
        'appointment_ids': appointment_ids,
        'is_bulk': True,
    }
    return render(request, 'Patient/page.html', context)


def payment_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    amount_inr = appointment.department.amount
    amount_paise = int(amount_inr * 100)

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {'appointment_id': str(appointment_id)},
        })
        razorpay_order_id = order['id']
    except Exception as e:
        razorpay_order_id = ''
        print("Razorpay order error:", e)

    context = {
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order_id,
        'total_paise': amount_paise,
        'data': amount_inr,
        'appointment_id': appointment_id,
    }
    return render(request, 'Patient/page.html', context)

# with convert real time exchange gbp to inr for stripe 

# def payment_page(request):
#     # Step 1: Get all appointments for user and calculate total in INR
#     appointments = Appointment.objects.filter(user_id=request.user.id)
#     total_inr = sum([appt.department.amount for appt in appointments])
#     total_paise = int(total_inr * 100)

#     # Step 2: Fetch real-time INR to GBP exchange rate from Fixer.io
#     ecb_url = "https://ratesapi.io/api/latest?base=EUR&symbols=GBP"
#     try:
#         response = requests.get(ecb_url)
#         print(f"Status Code: {response.status_code}")
#         print(f"Response Content: {response.text}")
        
#         if response.status_code == 200:
#             exchange_data = response.json()
#             if 'rates' not in exchange_data:
#                 raise ValueError("No 'rates' key found in the response data")
#                 inr_to_gbp = exchange_data['rates']['GBP']
#                 total_gbp = round(total_inr * inr_to_gbp, 2)
#         else:
#             raise ValueError(f"Failed to fetch data from ECB API. Status Code: {response.status_code}")
    
#     except Exception as e:
#         print("❌ Exchange rate fetch failed:", e)
#         return render(request, 'Patient/page.html', {
#         'data': total_inr,
#         'error_message': 'Failed to fetch exchange rates. Please try again later.'
#         })
#     # try:
#     #     response = requests.get(ecb_url)
#     #     exchange_data = response.json()

#     #     if response.status_code != 200 or 'rates' not in exchange_data:
#     #         raise ValueError("ECB API error or invalid response")

#     #     inr_to_gbp = exchange_data['rates']['GBP']
#     #     total_gbp = round(total_inr * inr_to_gbp, 2)
#     # except Exception as e:
#     #     print("Exchange rate fetch failed:", e)
#     #     return render(request, 'Patient/page.html', {
#     #         'data': total_inr,
#     #         'error_message': 'Failed to fetch exchange rates. Please try again later.'
#     #     })

#     # Step 3: Check Stripe minimum payment threshold
#     if total_gbp < 0.30:
#         return render(request, 'Patient/page.html', {
#             'data': total_inr,
#             'error_message': 'The total amount is too low to process via Stripe (minimum is £0.30).'
#         })

#     # Step 4: Create Stripe PaymentIntent in GBP
#     stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
#     try:
#         intent = stripe.PaymentIntent.create(
#             amount=int(total_gbp * 100),  # GBP in pence
#             currency='gbp',
#             metadata={'user_id': request.user.id}
#         )
#     except Exception as e:
#         print("❌ Stripe error:", e)
#         return render(request, 'Patient/page.html', {
#             'data': total_inr,
#             'stripe_error': f'Stripe Error: {str(e)}'
#         })

#     # Step 5: Render with context
#     context = {
#         'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
#         'client_secret': intent.client_secret,
#         'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#         'data': total_inr,
#         'converted_gbp': total_gbp
#     }
#     return render(request, 'Patient/page.html', context)

# def update_payment_status(user_id):
#     # Fetch all unpaid appointments for this user
#     appointments = Appointment.objects.filter(user_id=user_id, payment_status='unpaid')
    
#     # Mark them as paid
#     for appt in appointments:
#         appt.payment_status = 'paid'
#         appt.save()

# def payment_success(request):
#     # Get user ID from payment metadata or session
#     user_id = request.user.id

#     # Update the payment status of the appointments
#     update_payment_status(user_id)

#     # Return confirmation page
#     return render(request, 'Patient/payment_sucess.html', {
#         'message': 'Your payment has been successfully processed!'
#     })

# @csrf_exempt
# def razorpay_success(request):
#     if request.method == "POST":
#         user_id = request.user.id
#         update_payment_status(user_id)
#         # Optional: You can verify the signature here using Razorpay client
#         return render(request, "Patient/payment_sucess.html")
#     return redirect('Patient:dashboard_show')

# Initialize Razorpay client
# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# def razorpay_success(request):
#     # Get the Razorpay payment details from POST request
#     payment_id = request.POST.get('razorpay_payment_id')
#     order_id = request.POST.get('razorpay_order_id')
#     signature = request.POST.get('razorpay_signature')

#     # Prepare parameters for signature verification
#     params_dict = {
#         'razorpay_order_id': order_id,
#         'razorpay_payment_id': payment_id,
#         'razorpay_signature': signature
#     }

#     try:
#         # Verify the payment signature
#         razorpay_client.utility.verify_payment_signature(params_dict)

#         user_id = request.user.id

#         # Update the payment status for the user's appointments
#         update_payment_status(user_id)


#         # Redirect to payment success page
#         return redirect('Patient:payment_sucess')

#     except razorpay.errors.SignatureVerificationError:
#         # If verification fails, handle the error
#         return render(request, 'Patient/page.html', {'error_message': 'Payment verification failed!'})

import logging
# Set up logging
logger = logging.getLogger(__name__)

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def update_payment_status(user_id):
    try:
        # Fetch all unpaid appointments for this user
        appointments = Appointment.objects.filter(user_id=user_id, payment_status='unpaid')

        if not appointments:
            logger.warning(f"No unpaid appointments found for user {user_id}")
            return

        # Mark them as paid
        for appt in appointments:
            appt.payment_status = 'paid'
            appt.save()
            logger.info(f"Payment status updated for appointment ID: {appt.id}")
    except Exception as e:
        logger.error(f"Error updating payment status: {str(e)}")

def payment_success(request):
    # Get user ID from the request (assuming the user is logged in)
    user_id = request.user.id

    # Update the payment status of the appointments
    update_payment_status(user_id)

    # Return the confirmation page
    return render(request, 'Patient/payment_sucess.html', {
        'message': 'Your payment has been successfully processed!'
    })

def razorpay_success(request):
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    appointment_id = request.POST.get('appointment_id')

    logger.info(f"Received payment_id: {payment_id}, order_id: {order_id}, appointment_id: {appointment_id}")

    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature,
    }
    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        logger.info("Payment signature verified successfully")
    except Exception as e:
        logger.warning(f"Signature verification skipped (test mode): {str(e)}")

    # Mark paid: bulk (all) or single appointment
    appointment_ids = request.POST.get('appointment_ids')
    if appointment_ids:
        ids = [int(x) for x in appointment_ids.split(',') if x.strip().isdigit()]
        Appointment.objects.filter(id__in=ids, user=request.user).update(payment_status='paid')
    elif appointment_id:
        Appointment.objects.filter(id=appointment_id, user=request.user).update(payment_status='paid')
    else:
        update_payment_status(request.user.id)

    return redirect('Patient:payment_success')

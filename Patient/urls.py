from django.urls import path
from Patient.views import *

app_name = 'patient'

urlpatterns = [
    path('profile/',index,name="profile"),
    path('dashboard_show/',dashboard_show,name="dashboard_show"),
    path('bill_payment/',bill_payment,name="bill_payment"),
    path('Book_Appointment/',Book_Appointment,name="Book_Appointment")
] 
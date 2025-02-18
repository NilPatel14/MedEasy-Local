from django.urls import path
from Patient.views import *

app_name = 'patient'

urlpatterns = [
    path('profile/',index,name="profile"),
    path('dashboard_show/',dashboard_show,name="dashboard_show"),
    path('bill_payment/',bill_payment,name="bill_payment"),
    path('appointment/',Book_Appointment,name="Book_Appointment"),
    path('check_history/',check_history,name="check_history"),
    path('edit-profile/',edit_profile,name="edit-profile"),
    path('edit-appointment/<int:id>/',edit_appointment,name="edit-appointment"),
    path('delete-appointment/<int:id>/',delete_appointment,name="delete-appointment"),
    path('Check_Prescription_History',Check_Prescription_History,name="Check_Prescription_History"),
    path('Check_Appointment_History',Check_Appointment_History,name="Check_Appointment_History"),
] 
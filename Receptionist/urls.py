from django.urls import path
from Receptionist.views import *

app_name = 'receptionist'

urlpatterns = [
    path("profile/", index, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("AddPatientRecord/", AddPatientRecord, name="AddPatientRecord"),
    # path('get-patient-data/', get_patient_data, name='get_patient_data'),
    path("OPD/", OPD, name="OPD"),
    path("IPD/", IPD, name="IPD"),
    path("room/", room, name="room"),
    path("room_details/", room_details, name="room_details"),
    path('get-beds/', get_beds, name='get_beds'),
]

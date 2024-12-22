from django.urls import path
from .views import *

app_name = 'Doctor'

urlpatterns = [
    path('profile/',index,name="profile"),
    path('dashboard/',dashboard_show,name="dashboard"),
    path('prescription/',prescription_show,name="prescription")
]
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('log_in/',log_in_page,name="log_in"),
    path('log_out/',log_out,name="log_out"),
    path('profile/',profile,name="profile"),
    path('registrationurl/',register,name="registrationurl")
]
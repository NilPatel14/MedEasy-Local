from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "authorization"

urlpatterns = [
    path('', home, name="home"),
    path('log_in/', log_in_page, name="log_in"),
    path('log_out/', log_out, name="log_out"),
    path('profile/', profile, name="profile"),
    path('registrationurl/', register, name="registrationurl"),
    path('send-otp/', send_otp_email, name='send_otp_email'),

    # Password reset URLs
    # path('password_reset/', 
    #      auth_views.PasswordResetView.as_view(
    #          template_name='Home/password_reset_form.html',
    #          success_url=reverse_lazy('authorization:password_reset_done')
    #      ), 
    #      name='password_reset'),

    path('password_reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
         
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='Home/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Home/password_reset_confirm.html',
             success_url=reverse_lazy('authorization:password_reset_complete')  # ✅ Fixed Redirect!
         ), 
         name='password_reset_confirm'),

    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Home/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

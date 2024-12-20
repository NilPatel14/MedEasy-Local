from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.core.exceptions import ValidationError
import re

# Create your models here.
class ContactModel(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=25)
    contact_subject = models.CharField(max_length=20)
    contact_dis = models.CharField(max_length=100)

    def __str__(self):
        return self.contact_name

# ----USER TYPES---------
class usertypeModel(models.Model):
    usertype_id = models.IntegerField(primary_key=True)
    usertype = models.CharField(max_length=10)

    def __str__(self):
        return self.usertype
# ----------USER MODEL---------
class User(AbstractUser):
    # Custom fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    adhhar_no = models.CharField(max_length=12,unique=True)
    usertype = models.ForeignKey('usertypeModel',default=1, on_delete=models.CASCADE)

    # Remove password1 and password2 fields, use AbstractUser's password field
    
    # def validate_phone_no(self):
    #     """
    #     Validates the phone_no field to ensure it contains exactly 10 digits.
    #     """
    #     if self.phone_no:
    #         if not re.fullmatch(r'^\d{10}$', self.phone_no):
    #             raise ValidationError({'phone_no': 'Phone number must be exactly 10 digits.'})

    # # def validate_adhhar_no(self):
    # #     """
    # #     Validates the adhhar_no field to ensure it contains exactly 12 digits.
    # #     """
    # #     if self.adhhar_no:
    # #         if not re.fullmatch(r'^\d{12}$', str(self.adhhar_no)):
    # #             raise ValidationError({'adhhar_no': 'Aadhar number must be exactly 12 digits.'})

    # def clean(self):
    #     """
    #     Calls the individual validation methods for phone_no and adhhar_no.
    #     """
    #     self.validate_phone_no()
    #     # Validate the length and format of adhhar_no
        

    def __str__(self):
        return self.username
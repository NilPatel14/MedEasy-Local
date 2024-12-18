from django.db import models
from django.contrib.auth.models import User,AbstractUser
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
    gender = models.CharField(
        max_length=20,
        choices=(('male', 'Male'), ('female', 'Female'))
    )

    # Remove password1 and password2 fields, use AbstractUser's password field
    
    def __str__(self):
        return self.username
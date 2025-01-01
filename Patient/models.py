from django.db import models
from authorization.models import *
# from django.contrib.auth.models import User



class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=30)
    doc_id  = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.dept_name

# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE) 
    symptoms = models.CharField(max_length=200)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()

    def __str__(self):
        return self.name," : ",self.department



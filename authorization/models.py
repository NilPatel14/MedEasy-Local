from django.db import models

# Create your models here.

class ContactModel(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=25)
    contact_subject = models.CharField(max_length=20)
    contact_dis = models.CharField(max_length=100)

    def __str__(self):
        return self.contact_name



class usertypeModel(models.Model):
    usertype_id = models.IntegerField(primary_key=True)
    usertype = models.CharField(max_length=10)

    def __str__(self):
        return self.usertype


# class UserModel(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=10)
#     password = models.CharField(max_length=7)
#     first_name = models.CharField(max_length=10)
#     last_name = models.CharField(max_length=10)
#     email = models.EmailField(max_length=25)
#     mobileno = models.CharField(max_length=10,null=True)
#     usertype_id = models.ForeignKey(usertypeModel, on_delete=models.CASCADE)
    

#     def __str__(self):
#         return self.username
    

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)  # Unique usernames
    password = models.CharField(max_length=128)  # Longer for hashed passwords
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)  # Unique emails
    mobileno = models.CharField(max_length=15, null=True, blank=True)  # Supports international numbers
    usertype = models.ForeignKey(usertypeModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

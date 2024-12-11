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
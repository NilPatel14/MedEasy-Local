from django.db import models
from django.utils.timezone import now
from Patient.models import Appointment

class Prescription(models.Model):
    prescription_id = models.CharField(max_length=255, unique=True,)
    patient_name = models.CharField(max_length=255)
    patient_age = models.IntegerField()
    gender = models.CharField(max_length=250)
    diagnosis = models.CharField(max_length=255)
    medication = models.CharField(max_length=255)
    problem = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    prescription_details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    ipd_opd = models.CharField(max_length=255)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.prescription_id:
            self.prescription_id = f"RX-{now().strftime('%Y%m%d%H%M%S')}"
        super(Prescription, self).save(*args, **kwargs)

    def __str__(self):
        return self.patient_name

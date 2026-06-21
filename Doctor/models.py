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
            prefix = 'IPD' if self.ipd_opd == 'IPD' else 'OPD'
            existing_ids = Prescription.objects.filter(
                prescription_id__startswith=f'{prefix}-'
            ).values_list('prescription_id', flat=True)
            max_num = 0
            for pid in existing_ids:
                try:
                    num = int(pid.split('-')[1])
                    if num > max_num:
                        max_num = num
                except (IndexError, ValueError):
                    pass
            self.prescription_id = f"{prefix}-{str(max_num + 1).zfill(2)}"

        super(Prescription, self).save(*args, **kwargs)

    def __str__(self):
        return self.patient_name

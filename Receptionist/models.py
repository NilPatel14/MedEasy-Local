from django.db import models

class PatientRecord(models.Model):
    date = models.DateField()
    ipd_count = models.IntegerField(default=0)
    opd_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - IPD: {self.ipd_count}, OPD: {self.opd_count}"

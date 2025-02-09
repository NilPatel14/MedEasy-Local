from django.db import models
from authorization.models import User

class PatientRecord(models.Model):
    date = models.DateField()
    ipd_count = models.IntegerField(default=0)
    opd_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - IPD: {self.ipd_count}, OPD: {self.opd_count}"

class Room_type(models.Model):
    name = models.CharField(max_length=100)
    charges = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    room_no = models.IntegerField()
    room_type = models.ForeignKey(Room_type, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    total_beds = models.IntegerField()

    def __str__(self):
        return f"Room No: {self.room_no} - {self.room_type.name} - {self.availability}"
    
class Bed(models.Model):
    bed_no = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Bed No: {self.bed_no} - Room No: {self.room.room_no} - {self.room.room_type.name} - {self.availability}"

class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.patient} - Room No: {self.room.room_no} - Bed No: {self.bed.bed_no} - Check In: {self.check_in} - Check Out: {self.check_out}"
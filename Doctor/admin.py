from django.contrib import admin
from .models import Prescription


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'prescription_id', 'patient_name', 'patient_age', 'gender', 'diagnosis',
        'medication', 'problem', 'duration', 'frequency', 'prescription_details',
        'created_at', 'ipd_opd', 'appointment_id'
    )
    search_fields = ('patient_name', 'diagnosis', 'medication', 'prescription_id')
    list_filter = ('ipd_opd', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Prescription, PrescriptionAdmin)
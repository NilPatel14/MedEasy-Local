from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Prescription


class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription
        fields = (
            'prescription_id', 'patient_name', 'patient_age', 'gender',
            'diagnosis', 'medication', 'problem', 'duration', 'frequency',
            'prescription_details', 'created_at', 'ipd_opd', 'appointment_id'
        )
        export_order = (
            'prescription_id', 'patient_name', 'patient_age', 'gender',
            'diagnosis', 'medication', 'problem', 'duration', 'frequency',
            'prescription_details', 'created_at', 'ipd_opd', 'appointment_id'
        )


@admin.register(Prescription)
class PrescriptionAdmin(ImportExportModelAdmin):
    resource_class = PrescriptionResource
    list_display = (
        'prescription_id', 'patient_name', 'patient_age', 'gender',
        'diagnosis', 'medication', 'problem', 'duration', 'frequency',
        'prescription_details', 'created_at', 'ipd_opd', 'appointment_id'
    )
    search_fields = ('prescription_id', 'patient_name', 'diagnosis', 'medication', 'problem')
    list_filter = (
        'ipd_opd',
        'gender',
        'created_at',
        'appointment_id__department',
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

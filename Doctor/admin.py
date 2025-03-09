# from django.contrib import admin
# from .models import Prescription


# class PrescriptionAdmin(admin.ModelAdmin):
#     list_display = (
#         'prescription_id', 'patient_name', 'patient_age', 'gender', 'diagnosis',
#         'medication', 'problem', 'duration', 'frequency', 'prescription_details',
#         'created_at', 'ipd_opd', 'appointment_id'
#     )
#     search_fields = ('patient_name', 'diagnosis', 'medication', 'prescription_id')
#     list_filter = ('ipd_opd', 'created_at')
#     ordering = ('-created_at',)

# admin.site.register(Prescription, PrescriptionAdmin)


from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Prescription

# Define a custom resource for Prescription model to enable export and import
class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription
        fields = ('prescription_id', 'patient_name', 'patient_age', 'gender', 
                  'diagnosis', 'medication', 'problem', 'duration', 'frequency', 
                  'prescription_details', 'created_at', 'ipd_opd', 'appointment_id')
        export_order = ('prescription_id', 'patient_name', 'patient_age', 'gender', 
                        'diagnosis', 'medication', 'problem', 'duration', 'frequency', 
                        'prescription_details', 'created_at', 'ipd_opd', 'appointment_id')

# Register the Prescription model with admin and enable import/export
@admin.register(Prescription)
class PrescriptionAdmin(ImportExportModelAdmin):
    resource_class = PrescriptionResource
    list_display = ('prescription_id', 'patient_name', 'patient_age', 'gender', 
                    'diagnosis', 'medication', 'problem', 'duration', 'frequency', 
                    'prescription_details', 'created_at', 'ipd_opd', 'appointment_id')
    search_fields = ('prescription_id', 'patient_name', 'diagnosis', 'medication')
    list_filter = ('ipd_opd',)

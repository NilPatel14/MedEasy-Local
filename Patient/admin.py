# from django.contrib import admin
# from .models import Department, Appointment

# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('dept_id', 'dept_name', 'amount')
#     search_fields = ('dept_name',)
#     ordering = ('dept_id',)

# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')
#     search_fields = ('name', 'city', 'state', 'department__dept_name')
#     list_filter = ('status', 'preferred_date', 'department')
#     ordering = ('-created_at',)

# admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Appointment, AppointmentAdmin)

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Department, Appointment

# Define a custom resource for Appointment model to enable export and import
class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment
        fields = ('id', 'name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')
        export_order = ('id', 'name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')

# Define DepartmentAdmin (unchanged)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'amount')
    search_fields = ('dept_name',)
    ordering = ('dept_id',)

# Define AppointmentAdmin with import/export functionality
class AppointmentAdmin(ImportExportModelAdmin):
    resource_class = AppointmentResource  # Link to AppointmentResource
    list_display = ('name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')
    search_fields = ('name', 'city', 'state', 'department__dept_name')
    list_filter = ('status', 'preferred_date', 'department')
    ordering = ('-created_at',)

# Register models with their respective admin classes
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Appointment, AppointmentAdmin)

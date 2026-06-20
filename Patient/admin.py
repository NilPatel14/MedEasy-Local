from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Department, Appointment


class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment
        fields = ('id', 'name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'payment_status', 'created_at')
        export_order = ('id', 'name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'payment_status', 'created_at')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'amount')
    search_fields = ('dept_name',)
    list_filter = ('dept_name',)
    ordering = ('dept_id',)


class AppointmentAdmin(ImportExportModelAdmin):
    resource_class = AppointmentResource
    list_display = ('id', 'name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'payment_status', 'created_at')
    search_fields = ('name', 'city', 'state', 'department__dept_name', 'user__username')
    list_filter = (
        'status',
        'payment_status',
        'gender',
        'department',
        'preferred_date',
        'created_at',
    )
    ordering = ('-created_at',)
    date_hierarchy = 'preferred_date'


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Appointment, AppointmentAdmin)

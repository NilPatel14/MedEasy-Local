from django.contrib import admin
from .models import Department, Appointment

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'amount')
    search_fields = ('dept_name',)
    ordering = ('dept_id',)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob', 'gender', 'city', 'state', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')
    search_fields = ('name', 'city', 'state', 'department__dept_name')
    list_filter = ('status', 'preferred_date', 'department')
    ordering = ('-created_at',)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Appointment, AppointmentAdmin)
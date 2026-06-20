from django.contrib import admin
from .models import PatientRecord, Room_type, Room, Bed, Booking


class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'ipd_count', 'opd_count')
    search_fields = ('date',)
    list_filter = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'charges')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'room_type', 'availability', 'total_beds')
    search_fields = ('room_no',)
    list_filter = ('availability', 'room_type')
    ordering = ('room_no',)


class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_no', 'room', 'availability')
    search_fields = ('bed_no',)
    list_filter = ('availability', 'room', 'room__room_type')
    ordering = ('bed_no',)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room', 'bed', 'check_in', 'check_out')
    search_fields = ('patient__username', 'patient__first_name', 'patient__last_name', 'room__room_no')
    list_filter = ('check_in', 'check_out', 'room__room_type')
    ordering = ('-check_in',)
    date_hierarchy = 'check_in'


admin.site.register(PatientRecord, PatientRecordAdmin)
admin.site.register(Room_type, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Booking, BookingAdmin)

from django.contrib import admin
from .models import PatientRecord, Room_type, Room, Bed, Booking


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'charges')
    search_fields = ('name',)
    ordering = ('name',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'room_type', 'availability', 'total_beds')
    list_filter = ('availability', 'room_type')
    ordering = ('room_no',)

class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_no', 'room', 'availability')
    list_filter = ('availability', 'room')
    ordering = ('bed_no',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room', 'bed', 'check_in', 'check_out')
    search_fields = ('patient__username', 'room__room_no', 'bed__bed_no')
    list_filter = ('check_in', 'check_out')
    ordering = ('-check_in',)

admin.site.register(Room_type, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Booking, BookingAdmin)
from django.contrib import admin
from .models import ContactModel, usertypeModel, User


# Register ContactModel

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'contact_name', 'contact_email', 'contact_subject')
    search_fields = ('contact_name', 'contact_email')

admin.site.register(ContactModel, ContactModelAdmin)

# Register usertypeModel
class UsertypeModelAdmin(admin.ModelAdmin):
    list_display = ('usertype_id', 'usertype')
    search_fields = ('usertype',)

admin.site.register(usertypeModel, UsertypeModelAdmin)

# Custom User Admin
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'phone_no', 'adhhar_no', 'usertype', 'department')
    search_fields = ('username', 'email', 'phone_no', 'adhhar_no')
    list_filter = ('usertype', 'department')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phone_no', 'adhhar_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'usertype', 'department')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_no', 'adhhar_no', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'usertype', 'department')
        }),
    )

admin.site.register(User, CustomUserAdmin)

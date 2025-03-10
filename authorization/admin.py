from django.contrib import admin
from .models import ContactModel, usertypeModel, User
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin

# Register ContactModel
class ContactModelAdmin(admin.ModelAdmin):
    
    list_display = ('contact_id', 'contact_name', 'contact_email', 'contact_subject')
    search_fields = ('contact_name', 'contact_email')
    list_filter = ('contact_subject','contact_email')
    list_per_page = 10
# Register usertypeModel
class UsertypeModelAdmin(admin.ModelAdmin):
    list_display = ('usertype_id', 'usertype')
    search_fields = ('usertype',)


# Custom User Admin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'phone_no', 'adhhar_no', 'usertype', 'department')
    search_fields = ('username', 'email', 'phone_no', 'adhhar_no')
    list_filter = ('usertype', 'department')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_no', 'adhhar_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'usertype', 'department')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_no', 'adhhar_no', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'is_doctor', 'is_receptionist', 'is_patient', 'usertype', 'department')
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(usertypeModel, UsertypeModelAdmin)
admin.site.register(ContactModel, ContactModelAdmin)
admin.site.unregister(Group)
admin.site.unregister(Site)
# Custom Admin Site Header
admin.site.site_header = 'MedEasy Hospital Admin'
admin.site.site_title = 'MedEasy Hospital Admin'
admin.site.index_title = 'Welcome to MedEasy Hospital Admin'

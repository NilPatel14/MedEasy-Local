from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


from .models import User  # Import your custom User model

# Register the custom User model
class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_no', 'adhhar_no', 'usertype'),
        }),
    )

    # Define the fields to be displayed when viewing/editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_no', 'adhhar_no','usertype' )}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Specify the fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_no', 'adhhar_no', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_no', 'adhhar_no')
    ordering = ('username',)

# Register the custom UserAdmin with the User model
admin.site.register(User, CustomUserAdmin)
admin.site.register(ContactModel)
# admin.site.register(User)
admin.site.register(usertypeModel)
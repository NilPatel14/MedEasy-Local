from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


from .models import User  # Import your custom User model

# Register the custom User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets  # Use the default UserAdmin fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(User, CustomUserAdmin)
admin.site.register(ContactModel)
# admin.site.register(User)
admin.site.register(usertypeModel)
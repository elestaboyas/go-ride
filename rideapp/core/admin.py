from django.contrib import admin
from .models import Ride, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields':('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

admin.site.register(User, UserAdmin)
admin.site.register(Ride)
    

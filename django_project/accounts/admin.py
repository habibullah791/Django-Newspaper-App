from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]
    
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),) #  edit and add new custom fields, like age
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),) # for fields used when creating a user
    
    
    
admin.site.register(CustomUser, CustomUserAdmin)
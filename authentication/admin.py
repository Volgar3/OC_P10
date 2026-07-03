from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informations SoftDesk",
            {"fields": ("age", "can_be_contacted", "can_data_be_shared")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informations SoftDesk",
            {"fields": ("age", "can_be_contacted", "can_data_be_shared")},
        ),
    )


admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ["telegram_username"]
    list_display = ["telegram_username", "email", "full_name", "is_staff"]
    fieldsets = (
        (None, {"fields": ("telegram_username", "password")}),
        ("Personal info", {"fields": ("full_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

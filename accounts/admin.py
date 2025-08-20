from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User   # import your custom User model

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # what fields to show in admin list view
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)

    # allow editing groups and permissions
    filter_horizontal = ("groups", "user_permissions")

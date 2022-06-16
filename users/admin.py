from django.contrib import admin
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm


@admin.register(User)
class UserAdminConfig(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('username', 'email', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')

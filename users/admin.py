from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdminConfig(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('username', 'email', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserUser


class UserUserAdmin(UserAdmin):
    model = UserUser


admin.site.register(UserUser, UserUserAdmin)

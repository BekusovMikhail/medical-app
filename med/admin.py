from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    ordering = ('email',)


admin.site.register(User, UserAdmin)
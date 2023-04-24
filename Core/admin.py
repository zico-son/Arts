from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Core.models import User

class UserAdmin(BaseUserAdmin):
    pass
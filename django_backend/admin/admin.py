
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register only if the user model is not already registered.
if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)
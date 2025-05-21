from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating new users in the admin panel.
    Ensures passwords are hashed and phone_number is used as the USERNAME_FIELD.
    """
    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "username", "is_active", "is_staff", "is_superuser")

    def save(self, commit=True):
        # Ensure the password is hashed using set_password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for updating existing users in the admin panel.
    Ensures phone_number is handled correctly and password updates are hashed.
    """
    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "username", "is_active", "is_staff", "is_superuser")

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the User model.
    Uses custom forms and configures fields for phone_number as USERNAME_FIELD.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Fields to display in the admin list view
    list_display = ("phone_number", "full_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("phone_number", "first_name", "last_name", "username")
    ordering = ("phone_number",)

    # Fields for editing an existing user
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "username")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "password1", "password2", "first_name", "last_name", "username", "is_active", "is_staff", "is_superuser"),
        }),
    )

    # Ensure phone_number is used as the USERNAME_FIELD
    filter_horizontal = ()

# Register the User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    """Manager for accounts.models.User model"""

    use_in_migrations = True

    def _normalize_phone_number(phone_number:str):
        return phone_number.replace(" ", "")
    
    
    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError("The given phone number must be set")
        
        phone_number = self._normalize_phone_number(phone_number)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.username = phone_number
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)


    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


phone_validator = RegexValidator(
    regex=r"^(\+98|0)\s?([1-8]\d{9}|9\d{9})$",
    message="Phone number must be entered in the format: "
    "'+989xxxxxxxxx'. Up to 14 digits allowed.",
)


class User(AbstractUser):
    
    phone_number = models.CharField(
        _("phone number"),
        validators=[phone_validator],
        max_length=13,
        unique=True,
        null=False,
        blank=False
    )
        
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    def __str__(self):
        return f'{self.full_name}'
    
    USERNAME_FIELD = "phone_number"
    
    objects = UserManager()


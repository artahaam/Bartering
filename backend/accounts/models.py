from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):

    def _normalize_phone_number(self, phone_number:str):
        phone_number.replace(" ", "")
        if phone_number.startswith('+98'):
            phone_number = '0' + phone_number[3:]
        return phone_number
    

    def create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError(_("شماره تلفن الزامی است"))
        phone_number = self._normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, password, **extra_fields)


phone_validator = phone_validator = RegexValidator(
        regex=r"^09\d{9}$",
        message=_("شماره وارد شده معتبر نیست")
    )

student_id_validator = RegexValidator(
        regex=r"^40\d{7}$",
        message=_("شماره دانشجویی معتبر نیست")
)


class User(AbstractUser):
    
    phone_number = models.CharField(
        _("شماره تلفن"),
        validators=[phone_validator],
        max_length=13,
        unique=True,
        null=False,
        blank=False
    )
    
    student_id = models.CharField(
        _("شماره دانشجویی"),
        max_length=9,
        unique=True,
        validators=[student_id_validator],
        help_text=_("الزامی است، شروع با 40"),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
        
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    def __str__(self):
        return f'{self.phone_number}'
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['student_id']
    objects = UserManager()

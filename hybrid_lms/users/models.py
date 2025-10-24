from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, name, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        if not name:
            raise ValueError('Name field must be set')

        email = self.normalize_email(email)
        user_id = self.generate_user_id()
        if password is None:
            password = self.generate_random_password()

        user = self.model(
            user_id=user_id,
            name=name,
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, phone_number, password, **extra_fields)

    def generate_user_id(self):
        prefix = "USR"
        last_user = self.model.objects.order_by('-id').first()
        next_num = 1 if not last_user else last_user.id + 1
        return f"{prefix}{next_num:05d}"

    def generate_random_password(self, length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255,null=False, blank=False, default='TempUser')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")],
        blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.user_id

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expiry = timezone.now() + timedelta(minutes=5)
        self.save()
        return self.otp_code

    def verify_otp(self, otp):
        return self.otp_code == otp and self.otp_expiry and self.otp_expiry > timezone.now()

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", CustomUser.Role.ADMIN)
        return self._create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "User"
        COUNSELOR = "counselor", "Counselor"
        ADMIN = "admin", "Admin"

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    dob = models.DateField(blank=True, null=True)

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    # Counselor-specific fields
    specialization = models.CharField(max_length=255, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_counselor_active = models.BooleanField(default=True)
    # Availability stored as a list of {day, start, end} objects, e.g. [{"day":"Mon","start":"09:00","end":"12:00"}]
    availability = models.JSONField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Keep Django admin consistent for staff/superuser based on role
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


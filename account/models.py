# Create your models here.
"""Creating a user model for authentication"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Modifying default django model"""
    
    def create_user(self, email, password=None, **extra_fields):
        """creating a new user instance """

        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """creating a new superuser instance """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


bvn_validator = RegexValidator(
    regex=r'^\d{11}$',
    message='BVN must be an 11-digit number'
    )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model attributes"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255, blank=False)
    bvn = models.IntegerField(unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['bvn', 'email', 'password', 'phone_number']
    
    # Provide unique related_name values for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users_groups',  # Provide a unique related_name
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions',  # Provide a unique related_name
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.email

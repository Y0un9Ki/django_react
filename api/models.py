import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    # These fields tie to the roles!
    ADMIN = 1
    MANAGER = 2
    COMMON_USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (COMMON_USER, 'common_user')
    )
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    # Roles created here
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    username = models.CharField(unique=True, blank=False, max_length=10)
    location = models.CharField(max_length=100, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['location']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
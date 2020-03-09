from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from shared.models.base_model import BaseModel


class User(AbstractBaseUser, BaseModel):
    """Model for a user in the system"""

    class Meta:
        """Class to add more information on user model"""
        ordering = ('username',)

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    role_id = models.OneToOneField(
        'Role',
        on_delete=models.SET_NULL,
        related_name="user",
        null=True,
    )

    def __str__(self):
        return self.username


class Role(BaseModel):
    """Model for a user role"""
    type = models.CharField(max_length=10)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return self.type


class Permission(BaseModel):
    """Model for permissions available to a role"""
    name = models.CharField(max_length=50)
    codename = models.CharField(max_length=20)
    role = models.ForeignKey(
        Role,
        related_name="permissions",
        on_delete=models.SET_NULL,
        null=True,
        )

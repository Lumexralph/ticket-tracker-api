"""Module containing the similar fields and operations of the models"""
from django.db import models


class BaseModel(models.Model):
    """
    Base model to implement common fields
    Attributes:
        created_at: Holds date/time for when an object was created.
        deleted: Holds status for soft-deleted objects.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        """Additional for the base"""
        abstract = True

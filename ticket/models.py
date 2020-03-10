from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from shared.models.base_model import BaseModel
from account.models import User


class Ticket(BaseModel):
    """Model for a ticket created by a user"""
    ENHANCEMENT = 'EN'
    BUGFIX = "BF"
    DEVELOPMENT = "DV"
    QUALITY_ASSURANCE = "QA"

    TICKET_TYPES = [
        (ENHANCEMENT, 'enhancement'),
        (BUGFIX, 'bugfix'),
        (DEVELOPMENT, 'development'),
        (QUALITY_ASSURANCE, 'quality assurance')
    ]

    class Meta:
        """Class Meta to add more information for the ticket model"""
        ordering = ('type',)

    creator = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User,
        related_name='assigned_tickets',
        on_delete=models.SET_NULL,
        null=True,
    )
    activated = models.BooleanField(default=False)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=2,
        choices=TICKET_TYPES,
        default=ENHANCEMENT,
    )
    complexity = models.IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(5)])
    estimated = models.IntegerField(validators=[MinLengthValidator(0)])


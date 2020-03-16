"""Module containing the ticket serializers"""

from rest_framework import serializers
from ticket.models import Ticket
from account.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    """Class to handle the serializing and deserializing of ticket data"""
    creator = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        """Class to add additional information to the serializer"""
        model = Ticket
        fields = '__all__'

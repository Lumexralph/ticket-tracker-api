"""Module containing the ticket views"""
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.forms import model_to_dict

from ticket.serializers import TicketSerializer
from ticket.models import Ticket
from account.models import User
from services.authenticate_user import token_required


class CreateTicket(mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @token_required
    def post(self, request, *args, **kwargs):
        data = self.create(request, *args, **kwargs)

        if data:
            headers = self.get_success_headers(data.data)
            return Response(data.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({
            'error': 'not authorized to create a ticket'
        }, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        role = request.user['data']['user_info']['role']['type']
        username = request.user['data']['user_info']['username']
        if role == 'user':
            # import pdb
            # pdb.set_trace()
            creator = User.objects.filter(username=username).first()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # TODO: A better way to save once, try using the user id in creator field
            ticket = serializer.save()
            ticket.creator = creator
            ticket.save()
            return serializer

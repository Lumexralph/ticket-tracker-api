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


class AssignTicketToAdmin(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @token_required
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        admin_id = kwargs.get('admin_id')
        current_user = request.user['data']['user_info']

        if current_user['role']['type'] != 'user':
            return Response({
                'error': 'Only a user can assign a ticket.'
            }, status=status.HTTP_403_FORBIDDEN)

        request_admin = User.objects.filter(pk=admin_id).first()
        if not request_admin:
            return Response({
                'error': 'Admin provided is not recognised in the system.'
            }, status=status.HTTP_404_NOT_FOUND)

        if request_admin.role.type != 'admin':
            return Response({
                'error': 'Admin provided is not an authorized admin.'
            }, status=status.HTTP_403_FORBIDDEN)

        # fetch the ticket
        request_ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not request_ticket:
            return Response({
                'error': 'Could not find the ticket'
            }, status=status.HTTP_404_NOT_FOUND)

        if request_ticket.creator.id != current_user['id']:
            return Response({
                'error': 'Cannot assign a ticket you didn\'t create.'
            }, status=status.HTTP_403_FORBIDDEN)

        request_ticket.assigned_to = request_admin
        request_ticket.save()

        #  assign the ticket to that admin
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

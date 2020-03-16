"""Module containing the ticket views"""
from rest_framework import generics, mixins, status
from rest_framework.response import Response

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
        ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not ticket:
            return Response({
                'error': 'Could not find the ticket'
            }, status=status.HTTP_404_NOT_FOUND)

        if ticket.creator.id != current_user['id']:
            return Response({
                'error': 'Cannot assign a ticket you didn\'t create.'
            }, status=status.HTTP_403_FORBIDDEN)

        ticket.assigned_to = request_admin
        ticket.save()
        serializer = TicketSerializer(ticket)
        data = {
            'data': serializer.data,
            'message': 'ticket assigned to admin successfully',
        }

        return Response(data, status=status.HTTP_200_OK)


class ListTicket(mixins.ListModelMixin,
                 generics.GenericAPIView):
    """View for listing all tickets"""
    serializer_class = TicketSerializer

    def get_queryset(self):
        """
        This should return a list of all the tickets
        for the currently authenticated user.
        """
        current_user = self.request.user['data']['user_info']

        if current_user['role']['type'] == 'user':
            return Ticket.objects.filter(creator__username=current_user['username'], deleted=False)
        elif current_user['role']['type'] == 'admin':
            return Ticket.objects.filter(assigned_to__username=current_user['username'], deleted=False)

    @token_required
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RejectTicket(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @token_required
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        current_user = request.user['data']['user_info']

        if current_user['role']['type'] != 'admin':
            return Response({
                'error': 'Only an admin can reject a ticket.'
            }, status=status.HTTP_403_FORBIDDEN)

        # fetch the ticket
        ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not ticket:
            return Response({
                'error': 'Could not find the ticket'
            }, status=status.HTTP_404_NOT_FOUND)

        ticket.deleted = True
        ticket.save()

        serializer = TicketSerializer(ticket)
        data = {
            'data': serializer.data,
            'message': 'ticket rejected successfully',
        }

        return Response(data, status=status.HTTP_200_OK)


class AcceptTicket(generics.UpdateAPIView):
    # TODO: refactor accept accept and reject view to DRY
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @token_required
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        current_user = request.user['data']['user_info']

        if current_user['role']['type'] != 'admin':
            return Response({
                'error': 'Only an admin can reject a ticket.'
            }, status=status.HTTP_403_FORBIDDEN)

        # fetch the ticket
        ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not ticket:
            return Response({
                'error': 'Could not find the ticket'
            }, status=status.HTTP_404_NOT_FOUND)

        ticket.activated = True
        ticket.save()
        serializer = TicketSerializer(ticket)
        data = {
            'data': serializer.data,
            'message': 'ticket accepted successfully',
        }

        return Response(data, status=status.HTTP_200_OK)

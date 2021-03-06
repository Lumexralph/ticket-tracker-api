"""Module containing the methods/classes that handles account route"""
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from account.models import User
from services.jwt_service import generate_token
from services.authenticate_user import token_required


class UserRegistration(mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        data = self.create(request, *args, **kwargs)
        user = data.save()
        user.set_password(request.data['password'])

        user.save()

        headers = self.get_success_headers(data.data)
        payload = {
            'username': data.data['username'],
            'id': data.data['id'],
        }
        token = generate_token(payload)
        headers['Authorization'] = token

        data = {
            'data': data.data,
            'message': 'signup successfully'
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return serializer


class UserLogin(mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer_instance = serializer(data=request.data)
        data = serializer_instance.login(request.data)
        headers = self.get_success_headers(serializer.data)

        if not data['error']:
            data = serializer(data)

            payload = {
                'username': data.data['username'],
                'id': data.data['id'],
                'role': data.data['role']
            }
            token = generate_token(payload)
            headers['Authorization'] = token

            data = {
                'data': data.data,
                'message': 'login successfully'
            }
            return Response(data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({
                'error': 'Invalid login credentials'
            }, status=status.HTTP_401_UNAUTHORIZED, headers=headers)

"""Module containing the account user serializers"""
from django.forms import model_to_dict
from rest_framework import serializers
from account.models import User, Role, Permission


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Class to handle the serializing and deserializing of user signup"""

    class Meta:
        """Class to add additional information to the serializer"""
        model = User
        exclude = ['password']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'codename']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = ['type', 'permissions']


class UserLoginSerializer(serializers.ModelSerializer):
    """Class to handle the serializing and deserializing of user login"""
    role = RoleSerializer(read_only=True)

    class Meta:
        """Class to add additional information to the serializer"""
        model = User
        exclude = ['password']

    def login(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = User.objects.filter(username=username).first()

        data = {
            'error': True
        }

        if user:
            result = user.check_password(password)

            if result:
                user_data = model_to_dict(user)
                user_data['role'] = model_to_dict(user.role)
                user_data['error'] = False
                return user_data

        return data


class UserSerializer(serializers.ModelSerializer):
    """Class to handle the serializing and deserializing of user details"""

    class Meta:
        """Class to add additional information to the serializer"""
        model = User
        exclude = ['password']
        extra_kwargs = {'username': {'required': False},
                        'password': {'required': False}}

"""Module containing the token requirement functions"""
from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from services.jwt_service import decode_token


def get_token(http_request):
    """Get token from request object
    Args:
        http_request (HTTPRequest): Http request object
    Returns:
        token (string): Token string
    """
    token = http_request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return {'message': 'No token provided in request header'}
    elif 'bearer' not in token.lower():
        return {'message': 'Wrong token supplied in header'}
    token = token.split(' ')[-1]
    return token


def token_required(func):
    """Function decorator that validates or checks token provided in a request
    """

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        instance, request = args
        valid_token = get_token(request)
        if isinstance(valid_token, dict) and valid_token.get('message'):
            return Response({
                'error': valid_token['message']
            }, status=status.HTTP_401_UNAUTHORIZED)
        decoded = decode_token(valid_token)

        if decoded['error']:
            return Response({
                'error': decoded['message']
            }, status=status.HTTP_401_UNAUTHORIZED)

        request.user = decoded
        args = (instance, request)

        return func(*args, **kwargs)

    return wrapper_func

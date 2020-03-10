"""Module contains the jwt operations"""
import datetime
import os

import jwt


def generate_token(payload, exp=12000):
    """
    Generates jwt tokens
    params:
        payload: The data to encode
        exp: Token Expiration. This could be datetime object or an integer
    result:
        token: This is the bearer token in this format 'Bearer token'
    """
    key = os.environ.get('JWT_SECRET')
    jwt_payload = jwt.encode({'user_info': payload,
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp)},
                             key, algorithm='HS256')

    return jwt_payload


def decode_token(token):
    """
    Decodes the provided token
    Argument:
        token: the jwt encoded token
    Returns:
        dict: the decoded token
    Raises:
        raises jwt error if the token failed verification
    """
    key = os.environ.get('JWT_SECRET')
    result = {
        'error': True,
        'data': None,
        'message': None,
    }

    try:
        decoded = jwt.decode(token, key, algorithms='HS256')
        result['error'] = False
        result['data'] = decoded
    except jwt.exceptions.ExpiredSignatureError:
        result['message'] = 'Provided token has expired, try login again'
    except (jwt.exceptions.InvalidTokenError,
            jwt.exceptions.DecodeError):
        result['message'] = 'token  provided cannot be decoded because it failed validation'

    return result

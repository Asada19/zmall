import jwt
from datetime import datetime, timedelta
from rest_framework import exceptions
from django.conf import settings


def encode_jwt(payload):
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        json_encoder=None
    )

    return token


def decode_jwt(token):
    token = jwt.decode(
        jwt=token,
        key=settings.JWT_SECRET,
        algorithms=settings.JWT_ALGORITHM
    )

    return token


class Token:
    token_type = None
    lifetime = None

    def __init__(self, token=None):
        self.token = token

        self.payload = {'token_type': self.token_type}
        self.set_exp(start_time=datetime.now())
        self.set_iat(at_time=datetime.now())

    def set_exp(self, start_time):
        self.payload['exp'] = start_time + self.lifetime

    def check_exp(self, current_time):
        if current_time >= self.payload['exp']:
            raise exceptions.AuthenticationFailed('Token has expired')

    def set_iat(self, at_time):
        self.payload['iat'] = at_time

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __str__(self):
        return encode_jwt(self.payload)

    @classmethod
    def create(cls, user_id):
        token = cls()
        token['user'] = user_id
        return token


class AccessToken(Token):
    token_type = 'access'
    lifetime = timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME)


class RefreshToken(Token):
    token_type = 'refresh'
    lifetime = timedelta(minutes=settings.REFRESH_TOKEN_LIFETIME)

    @property
    def access_token(self):
        access = AccessToken()
        access.set_exp(start_time=datetime.now())
        access['token_type'] = 'access'
        access['user'] = self.payload['user']
        access.set_iat(at_time=datetime.now())

        return access

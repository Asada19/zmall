from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework import exceptions

from api_auth.tokens import RefreshToken, AccessToken, decode_jwt

User = get_user_model()

class TokenObtainSerializer(serializers.Serializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField()

    def validate(self, attrs):

        authenticate_kwargs = {
            "email": attrs["email"],
            "password": attrs["password"],
        }

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if not user:
            raise exceptions.AuthenticationFailed("There is no such user listed in system")

        refresh = self.get_token(user.id)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data

    @classmethod
    def get_token(cls, user_id):
        return cls.token_class.create(user_id)


class AccessTokenObtainSerializer(serializers.Serializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['refresh'] = serializers.CharField()

    def validate(self, attrs):
        token = decode_jwt(attrs["refresh"])
        token_class = RefreshToken(token=token)
        refresh = token_class.create(token['user'])
        data = {"access": str(refresh.access_token)}

        return data


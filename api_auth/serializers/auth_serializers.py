import re
import google
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.conf import settings

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], password=validated_data['password'],
                                          first_name=validated_data['first_name'],
                                          last_name=validated_data['last_name'])
        return user

    def validate(self, attrs):
        pass_pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        name_pattern = "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"

        if not re.match(name_pattern, attrs['first_name']) or not re.match(name_pattern, attrs['last_name']):
            raise serializers.ValidationError('Your name can consist only of letters and \'-. characters.')

        if not re.match(pass_pattern, attrs['password']):
            raise serializers.ValidationError('Your password should consist of minimum 8 characters, '
                                              'at least 1 letter and 1 number.')

        return attrs


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def is_valid(self, *, raise_exception=False):
        # Checking if entered credentials are valid

        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active',)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = get_user_model().objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = get_user_model().objects.filter(email=email).first()
        return user


class ConfirmPasswordResetSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("The new passwords fields did not match.")
        return data

    def save(self):
        user = self.context['user']
        new_password = self.validated_data['new_password1']
        if user.check_password(new_password):
            raise serializers.ValidationError("Old and new passwords match. There is no need to reset the password.")
        user.set_password(new_password)
        user.save()


class GoogleSocialAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs['error']:
            raise exceptions.AuthenticationFailed(attrs['error'])

        user_data = google.Google.validate(attrs['code'])
        try:
            user_data["sub"]
        except Exception as _:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data["aud"] != settings["GOOGLE_CLIENT_ID"]:
            raise exceptions.AuthenticationFailed("Unrecognized google client")

        return attrs

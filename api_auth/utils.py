import requests
from django.conf import settings
from rest_framework import exceptions


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise exceptions.AuthenticationFailed('Failed to obtain access token from Google.')

    access_token = response.json()['access_token']

    return access_token


def google_get_user_info(access_token: str):
    url = f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}'
    response = requests.get(url)
    return response

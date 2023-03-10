from datetime import datetime
import jwt
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from django.conf import settings

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return None
        return self.authenticate_credentials(access_token)

    def authenticate_credentials(self, token):
        if isinstance(token, bytes):
            token = token.decode("ascii")
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user_id = data["user_id"]
            user = User.objects.get(id=user_id)   

        except (jwt.DecodeError, jwt.InvalidAlgorithmError, AttributeError):
            raise exceptions.AuthenticationFailed("Invalid Token")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")
        return user, None

        
import jwt
import datetime
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token  # Import the Token model

CustomUser = get_user_model()

class TokenAuthentication(BaseAuthentication):
    """
    Custom Token Authentication using JWT.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            token_obj = Token.objects.get(token=token, is_active=True)
            if token_obj.has_expired():
                token_obj.deactivate()
                raise AuthenticationFailed('Token has expired')
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token not found or inactive')

        try:
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, token)

    @staticmethod
    def generate_jwt(user):
        """
        Generate JWT for a given user and store it in the database.
        """
        expiration = timezone.now() + datetime.timedelta(days=1)
        payload = {
            'user_id': str(user.id),
            'exp': expiration,
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Save the token in the database
        Token.objects.create(user=user, token=token, expires_at=expiration)

        return token

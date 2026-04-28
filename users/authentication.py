from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from .utils import decode_token

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
        except:
            raise AuthenticationFailed('Invalid token format')

        payload = decode_token(token)

        if not payload:
            raise AuthenticationFailed('Invalid or expired token')

        user = User.objects(id=payload['user_id']).first()

        if not user:
            raise AuthenticationFailed('User not found')

        return (user, None)
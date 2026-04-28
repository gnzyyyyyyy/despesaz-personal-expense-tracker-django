from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from .utils import decode_token

def auth_middleware(get_response):
    def middleware(request):
        token = None

         # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except:
                pass
        
        # Get token from cookie
        if not token:
            token = request.COOKIES.get('token')
        
        if not token:
            request.user = None
            return get_response(request)

        try:
            payload = decode_token(token)
            user = User.objects(id=payload['user_id']).first()

            if not user:
                raise AuthenticationFailed('User not found')
            
            request.user = user

        except Exception as e:
            raise AuthenticationFailed('Unauthenticated') from e

        return get_response(request)

    return middleware
           
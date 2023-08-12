import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from tracker.models import AuthUser


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "").split()
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(
                detail="Invalid authentication header. No authentication header."
            )

        user = jwt.decode(
            auth[1], settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        try:
            user = AuthUser.objects.get(public_id=user.get("public_id"))
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return user, None

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from accounting.models import AuthUser


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "").split()
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(detail="No authentication header.")

        try:
            user = jwt.decode(
                auth[1], settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except:
            raise exceptions.AuthenticationFailed(
                detail="Invalid authentication header"
            )

        try:
            user, _ = AuthUser.objects.get_or_create(public_id=user.get("public_id"))
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return user, None

from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from accounting.models import Account


def auth_decorator(function):
    @wraps(function)
    def wrapped_function(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get("pk")
        if pk:
            account = Account.objects.get(pk=kwargs.get("pk"))
            if not user == account.user and user.role not in [
                "manager",
                "admin",
            ]:
                return Response(
                    "You can not perform this action", status=status.HTTP_403_FORBIDDEN
                )
        else:
            if user.role not in ["manager", "admin"]:
                return Response(
                    "You can not perform this action", status=status.HTTP_403_FORBIDDEN
                )
        return function(self, request, *args, **kwargs)

    return wrapped_function

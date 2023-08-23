from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounting.models import Account, AuditLog
from accounting.permissions import auth_decorator
from accounting.serializers import AccountSerializer, AuditLogSerializer


class AccountViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    @auth_decorator
    def accounts(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        user = request.user
        if user.role in ["manager", "admin"]:
            accounts = Account.objects.all()
            response = []
            for account in accounts:
                response.append(
                    {
                        "account": AccountSerializer(account).data,
                        "logs": AuditLogSerializer(
                            AuditLog.objects.filter(user=account.user), many=True
                        ).data,
                    }
                )
            return Response(response, status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(user=user)
            logs = AuditLog.objects.filter(user=user)
            return Response(
                {
                    "account": AccountSerializer(account).data,
                    "logs": AuditLogSerializer(logs, many=True).data,
                },
                status=status.HTTP_200_OK,
            )

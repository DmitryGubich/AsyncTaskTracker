from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounting.models import Account, AuditLog, Balance, Task
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

    @action(detail=False, methods=["get"])
    @auth_decorator
    def analytics(self, request):
        completed_prices = list(
            Task.objects.filter(status="done").values_list("fee", flat=True)
        )
        in_progress_prices = list(
            Task.objects.filter(status="in_progress").values_list("price", flat=True)
        )

        today_profit = sum(in_progress_prices) - sum(completed_prices)

        accounts_with_negative_balance = []
        for account in Account.objects.all():
            if account.balance < 0:
                accounts_with_negative_balance.append(account)

        return Response(
            {
                "today_profit": today_profit,
                "accounts_with_negative_balance": len(accounts_with_negative_balance),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="top-task")
    @auth_decorator
    def top_task(self, request):
        day = self.request.query_params.get("date") or datetime.today().strftime(
            "%Y-%m-%d"
        )
        task = (
            Task.objects.filter(status="done", assigned_date=day)
            .order_by("-price")
            .first()
        )
        if task:
            return Response(
                {
                    "public_id": task.public_id,
                    "description": task.description,
                    "price": task.price,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                "There are no finished tasks",
                status=status.HTTP_200_OK,
            )

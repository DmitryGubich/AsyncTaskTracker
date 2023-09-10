from datetime import datetime

from django.db.models import F, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.models import Balance, Task
from analytics.permissions import auth_decorator


class AnalyticsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    @auth_decorator
    def analytics(self, request):
        completed_fees = sum(
            Task.objects.filter(status="done").values_list("fee", flat=True)
        )
        in_progress_prices = sum(
            Task.objects.filter(status="in_progress").values_list("price", flat=True)
        )

        today_profit = in_progress_prices - completed_fees

        accounts_with_negative_balance = (
            Balance.objects.values("account")
            .annotate(balance=Sum(F("credit") - F("debit")))
            .filter(balance__lt=0)
            .count()
        )

        return Response(
            {
                "today_profit": today_profit,
                "accounts_with_negative_balance": accounts_with_negative_balance,
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
                    "jira_id": task.jira_id,
                    "price": task.price,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                "There are no finished tasks",
                status=status.HTTP_200_OK,
            )

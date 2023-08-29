import random

from async_task_tracker_schemas.events import Tracker
from producer import publish
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tracker.models import AuthUser, Task
from tracker.permissions import auth_decorator
from tracker.serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer

    def list(self, request):
        user = request.user
        if user.role in ["manager", "admin"]:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assignee=user)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @auth_decorator
    def retrieve(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        serializer = self.serializer_class(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @auth_decorator
    def destroy(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["put"])
    @auth_decorator
    def complete(self, request, pk):
        fee = random.randint(20, 40)
        task = Task.objects.get(pk=pk)
        task.status = "done"
        task.fee = fee
        task.save()
        serializer = self.serializer_class(task)

        publish(
            event={
                "event": Tracker.TASK_COMPLETED,
                "body": {
                    "public_id": str(task.public_id),
                    "description": str(task.description),
                    "jira_id": str(task.jira_id),
                    "status": task.status,
                    "assignee": str(task.assignee),
                    "fee": str(task.fee),
                    "price": str(task.price),
                },
                "version": "3",
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    @auth_decorator
    def shuffle(self, request):
        in_progress_tasks = Task.objects.filter(status="in_progress")
        for task in in_progress_tasks:
            task.assignee = AuthUser.objects.exclude(
                role__in=["manager", "admin"]
            ).order_by("?")[0]
            task.save()
            publish(
                event={
                    "event": Tracker.TASK_ASSIGNED,
                    "body": {
                        "public_id": str(task.public_id),
                        "description": task.description,
                        "jira_id": task.jira_id,
                        "status": task.status,
                        "assignee": str(task.assignee),
                        "fee": str(task.fee),
                        "price": str(task.price),
                    },
                    "version": "3",
                }
            )
        serializer = self.serializer_class(in_progress_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from async_task_tracker_schemas.events import Tracker
from producer import publish
from rest_framework import serializers

from tracker.models import AuthUser, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = [
            "id",
            "public_id",
            "description",
            "jira_id",
            "status",
            "assignee",
            "price",
            "fee",
        ]

        read_only_fields = ["id", "public_id", "assignee", "price", "fee"]

    def create(self, validated_data):
        validated_data["assignee"] = AuthUser.objects.exclude(
            role__in=["manager", "admin"]
        ).order_by("?")[0]
        task = Task.objects.create(**validated_data)

        publish(
            event={
                "event": Tracker.TASK_ASSIGNED,
                "body": {
                    "public_id": str(task.public_id),
                    "description": task.description,
                    "jira_id": task.jira_id,
                    "status": task.status,
                    "assignee": str(task.assignee),
                    "price": str(task.price),
                    "fee": str(task.fee),
                },
                "version": "3",
            }
        )

        return task

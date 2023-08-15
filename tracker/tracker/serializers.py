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
            "status",
            "assignee",
        ]

        read_only_fields = ["id", "public_id", "assignee"]

    def create(self, validated_data):
        validated_data["assignee"] = AuthUser.objects.exclude(
            role__in=["manager", "admin"]
        ).order_by("?")[0]
        task = Task.objects.create(**validated_data)

        publish(
            event="Task.Assigned",
            body={
                "public_id": str(task.public_id),
                "assignee": str(task.assignee),
            },
        )

        return task

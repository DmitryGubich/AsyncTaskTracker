from rest_framework import serializers

from tracker.models import Task


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

        read_only_fields = ["id", "public_id"]

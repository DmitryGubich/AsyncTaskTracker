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
        return super().create(validated_data)

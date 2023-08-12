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
        validated_data["assignee"] = AuthUser.objects.order_by("?")[0]
        return Task.objects.create(**validated_data)

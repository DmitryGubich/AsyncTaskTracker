from rest_framework import serializers

from accounting.models import Account, AuditLog


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = [
            "id",
            "public_id",
            "user",
            "balance",
        ]

        read_only_fields = ["id", "public_id", "user", "balance"]


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog

        fields = [
            "id",
            "user",
            "date_created",
            "description",
        ]

        read_only_fields = ["id", "user", "date_created", "description"]

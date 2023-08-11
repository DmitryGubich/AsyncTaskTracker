from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User

        fields = [
            "public_id",
            "username",
            "password",
            "role",
        ]

        read_only_fields = ["public_id"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], role=validated_data["role"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

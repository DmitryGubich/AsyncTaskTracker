from django.contrib.auth import get_user_model
from producer import publish
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def list(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("user_created", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("user_updated", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        publish("user_deleted", str(user.public_id))
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

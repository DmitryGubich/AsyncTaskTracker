from rest_framework import generics
from rest_framework.permissions import AllowAny

from tracker.models import Task
from tracker.serializers import TaskSerializer


class TaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TaskSerializer

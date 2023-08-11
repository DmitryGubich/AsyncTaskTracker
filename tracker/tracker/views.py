from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.models import Task
from tracker.serializers import TaskSerializer


class TaskView(APIView):
    serializer_class = TaskSerializer

    def get(self, request):
        tasks = Task.objects.all()
        tasks_serializer = self.serializer_class(tasks, many=True)
        return Response(tasks_serializer.data, status=status.HTTP_200_OK)

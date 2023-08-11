from django.urls import path

from tracker.views import TaskView

urlpatterns = [
    path("tasks/", TaskView.as_view(), name="tasks"),
]

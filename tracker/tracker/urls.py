from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tracker.views import TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]

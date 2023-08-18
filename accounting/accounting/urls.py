from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounting.views import AccountViewSet

router = DefaultRouter()
router.register("", AccountViewSet, basename="accounting")

urlpatterns = [
    path("", include(router.urls)),
]

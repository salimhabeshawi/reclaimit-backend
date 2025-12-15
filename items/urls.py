from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactRequestViewSet, ItemPostViewSet

router = DefaultRouter()
router.register(r"items", ItemPostViewSet, basename="items")
router.register(r"requests", ContactRequestViewSet, basename="requests")

urlpatterns = [
    path("", include(router.urls)),
]

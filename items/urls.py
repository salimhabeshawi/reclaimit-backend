from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemPostViewSet, ContactRequestViewSet

router = DefaultRouter()
router.register(r'items', ItemPostViewSet, basename='items')
router.register(r'requests', ContactRequestViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),
]

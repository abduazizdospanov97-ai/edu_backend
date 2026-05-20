from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet

router = DefaultRouter()
router.register('', TestViewSet, basename='tests')

urlpatterns = [path('', include(router.urls))]

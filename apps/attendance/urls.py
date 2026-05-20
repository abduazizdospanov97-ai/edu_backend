from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, AttendanceBulkView, AttendanceStatsView

router = DefaultRouter()
router.register('', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('bulk/', AttendanceBulkView.as_view(), name='attendance-bulk'),
    path('stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('', include(router.urls)),
]

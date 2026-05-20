from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response({'success': True, 'data': CourseSerializer(qs, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({'success': True, 'data': CourseSerializer(obj).data})

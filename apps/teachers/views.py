from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer, TeacherUpdateSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TeacherUpdateSerializer
        return TeacherSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response({'success': True, 'data': TeacherSerializer(qs, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({'success': True, 'data': TeacherSerializer(obj).data})

    def create(self, request, *args, **kwargs):
        serializer = TeacherCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({'success': True, 'data': TeacherSerializer(teacher).data}, status=201)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = TeacherUpdateSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({'success': True, 'data': TeacherSerializer(teacher).data})

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.user.delete()
        return Response({'success': True})

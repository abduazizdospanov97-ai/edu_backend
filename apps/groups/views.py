from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializer, GroupWriteSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related('course', 'teacher', 'room').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GroupWriteSerializer
        return GroupSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response({'success': True, 'data': GroupSerializer(qs, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({'success': True, 'data': GroupSerializer(obj).data})

    def create(self, request, *args, **kwargs):
        serializer = GroupWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'success': True, 'data': GroupSerializer(obj).data}, status=201)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = GroupWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'success': True, 'data': GroupSerializer(obj).data})

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({'success': True})

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        group = self.get_object()
        from apps.students.serializers import StudentSerializer
        students = group.student_set.filter(status='ACTIVE')
        return Response({'success': True, 'data': StudentSerializer(students, many=True).data})

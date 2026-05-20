from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Student
from .serializers import StudentSerializer, StudentWriteSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('course', 'group').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'course', 'group']
    search_fields = ['first_name', 'last_name', 'phone']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentWriteSerializer
        return StudentSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        return Response({'success': True, 'data': StudentSerializer(qs, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({'success': True, 'data': StudentSerializer(obj).data})

    def create(self, request, *args, **kwargs):
        serializer = StudentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'success': True, 'data': StudentSerializer(obj).data}, status=201)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = StudentWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'success': True, 'data': StudentSerializer(obj).data})

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({'success': True})

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        student = self.get_object()
        from apps.payments.serializers import PaymentSerializer
        payments = student.payment_set.order_by('-created_at')
        return Response({'success': True, 'data': PaymentSerializer(payments, many=True).data})

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        student = self.get_object()
        from apps.attendance.serializers import AttendanceSerializer
        records = student.attendance_set.order_by('-date')[:30]
        return Response({'success': True, 'data': AttendanceSerializer(records, many=True).data})

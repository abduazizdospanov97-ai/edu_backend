from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
from datetime import date, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer, PaymentWriteSerializer
from apps.students.models import Student


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('student', 'student__course').order_by('-created_at')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'method', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentWriteSerializer
        return PaymentSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        return Response({'success': True, 'data': PaymentSerializer(qs, many=True).data})

    def create(self, request, *args, **kwargs):
        serializer = PaymentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Update student balance
        student = serializer.validated_data['student']
        amount = serializer.validated_data['amount']
        student.balance += amount
        student.save()
        payment = serializer.save()
        return Response({'success': True, 'data': PaymentSerializer(payment).data}, status=201)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({'success': True})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        today = date.today()
        month_start = today.replace(day=1)
        week_start = today - timedelta(days=today.weekday())

        total_all = Payment.objects.filter(status='PAID').aggregate(s=Sum('amount'))['s'] or 0
        total_month = Payment.objects.filter(status='PAID', created_at__date__gte=month_start).aggregate(s=Sum('amount'))['s'] or 0
        total_week = Payment.objects.filter(status='PAID', created_at__date__gte=week_start).aggregate(s=Sum('amount'))['s'] or 0
        total_today = Payment.objects.filter(status='PAID', created_at__date=today).aggregate(s=Sum('amount'))['s'] or 0

        return Response({
            'success': True,
            'data': {
                'total': total_all,
                'month': total_month,
                'week': total_week,
                'today': total_today,
            }
        })


class DebtorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        min_debt = int(request.query_params.get('min_debt', 1))
        students = Student.objects.filter(balance__lt=-min_debt + 1).select_related('course', 'group')
        data = []
        for s in students:
            data.append({
                'id': s.id,
                'name': f"{s.first_name} {s.last_name}",
                'phone': s.phone,
                'course': s.course.name if s.course else None,
                'group': s.group.name if s.group else None,
                'balance': s.balance,
                'debt': abs(s.balance),
            })
        return Response({'success': True, 'data': data})

    def post(self, request):
        # Notify debtors (stub - without real SMS)
        student_ids = request.data.get('student_ids', [])
        notified = Student.objects.filter(id__in=student_ids, balance__lt=0).count()
        return Response({
            'success': True,
            'data': {
                'notified': notified,
                'message': f"{notified} ta qarzdorga xabar yuborildi (stub)"
            }
        })

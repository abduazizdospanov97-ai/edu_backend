from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from datetime import date
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.select_related('student', 'group').order_by('-date')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        group_id = request.query_params.get('group_id')
        att_date = request.query_params.get('date')
        if group_id:
            qs = qs.filter(group_id=group_id)
        if att_date:
            qs = qs.filter(date=att_date)
        return Response({'success': True, 'data': AttendanceSerializer(qs[:100], many=True).data})


class AttendanceBulkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_id = request.data.get('group_id')
        att_date = request.data.get('date')
        records = request.data.get('records', [])
        if not group_id or not att_date:
            return Response({'success': False, 'error': 'group_id va date kerak'}, status=400)
        created = 0
        for rec in records:
            obj, _ = Attendance.objects.update_or_create(
                student_id=rec['student_id'],
                group_id=group_id,
                date=att_date,
                defaults={'status': rec.get('status', 'PRESENT')}
            )
            created += 1
        return Response({'success': True, 'data': {'saved': created}})


class AttendanceStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_id = request.query_params.get('group_id')
        today = date.today()
        qs = Attendance.objects.filter(date=today)
        if group_id:
            qs = qs.filter(group_id=group_id)

        total = qs.count()
        present = qs.filter(status='PRESENT').count()
        absent = qs.filter(status='ABSENT').count()
        late = qs.filter(status='LATE').count()

        pct = round(present / total * 100) if total else 0

        return Response({
            'success': True,
            'data': {
                'total': total,
                'present': present,
                'absent': absent,
                'late': late,
                'percentage': pct,
            }
        })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta
from apps.students.models import Student
from apps.groups.models import Group
from apps.payments.models import Payment
from apps.attendance.models import Attendance


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()

        total_students = Student.objects.filter(status='ACTIVE').count()
        total_groups = Group.objects.count()
        total_debtors = Student.objects.filter(balance__lt=0).count()

        today_income = Payment.objects.filter(
            status='PAID', created_at__date=today
        ).aggregate(s=Sum('amount'))['s'] or 0

        # Bugungi davomat
        today_att = Attendance.objects.filter(date=today)
        att_total = today_att.count()
        att_present = today_att.filter(status='PRESENT').count()
        att_pct = round(att_present / att_total * 100) if att_total else 0

        return Response({
            'success': True,
            'data': {
                'total_students': total_students,
                'total_groups': total_groups,
                'total_debtors': total_debtors,
                'today_income': today_income,
                'attendance': {
                    'total': att_total,
                    'present': att_present,
                    'percentage': att_pct,
                }
            }
        })


class DashboardRevenueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'week')
        today = date.today()
        data = []

        if period == 'week':
            days = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sha', 'Ya']
            for i in range(6, -1, -1):
                d = today - timedelta(days=i)
                amount = Payment.objects.filter(
                    status='PAID', created_at__date=d
                ).aggregate(s=Sum('amount'))['s'] or 0
                data.append({'day': days[d.weekday()], 'date': str(d), 'amount': amount})

        elif period == 'month':
            for i in range(29, -1, -1):
                d = today - timedelta(days=i)
                amount = Payment.objects.filter(
                    status='PAID', created_at__date=d
                ).aggregate(s=Sum('amount'))['s'] or 0
                data.append({'day': str(d.day), 'date': str(d), 'amount': amount})

        return Response({'success': True, 'data': data})


class DashboardRecentPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.select_related(
            'student', 'student__course'
        ).filter(status='PAID').order_by('-created_at')[:10]

        data = []
        for p in payments:
            data.append({
                'id': p.id,
                'studentName': f"{p.student.first_name} {p.student.last_name}",
                'courseName': p.student.course.name if p.student.course else '',
                'amount': p.amount,
                'method': p.method,
                'date': p.created_at.isoformat(),
            })
        return Response({'success': True, 'data': data})

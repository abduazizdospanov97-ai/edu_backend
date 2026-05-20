from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'group', 'date', 'status']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

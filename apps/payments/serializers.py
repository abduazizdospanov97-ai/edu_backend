from rest_framework import serializers
from apps.students.models import Student
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'student', 'student_name', 'course_name',
                  'amount', 'method', 'status', 'note', 'created_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_course_name(self, obj):
        return obj.student.course.name if obj.student.course else None


class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'method', 'status', 'note']

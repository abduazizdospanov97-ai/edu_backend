from rest_framework import serializers
from apps.courses.serializers import CourseSerializer
from apps.rooms.serializers import RoomSerializer
from apps.teachers.serializers import TeacherSerializer
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'teacher', 'room',
                  'start_time', 'end_time', 'days', 'max_students', 'student_count']

    def get_student_count(self, obj):
        return obj.student_set.filter(status='ACTIVE').count()


class GroupWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

from rest_framework import serializers
from apps.courses.serializers import CourseSerializer
from apps.groups.models import Group
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    group_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone',
                  'birth_date', 'address', 'course', 'group', 'group_name',
                  'balance', 'status']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_group_name(self, obj):
        return obj.group.name if obj.group else None


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

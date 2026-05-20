from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.users.models import User
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'name', 'email', 'phone', 'salary', 'subject']

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email


class TeacherCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    salary = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Bu email allaqachon band.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            role='TEACHER',
        )
        teacher = Teacher.objects.create(
            user=user,
            phone=validated_data.get('phone', ''),
            salary=validated_data.get('salary', 0),
            subject=validated_data.get('subject', ''),
        )
        return teacher


class TeacherUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    salary = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.user.name = validated_data['name']
            instance.user.save(update_fields=['name'])
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        if 'salary' in validated_data:
            instance.salary = validated_data['salary']
        if 'subject' in validated_data:
            instance.subject = validated_data['subject']
        instance.save()
        return instance

from rest_framework import serializers
from .models import Test, TestResult, Question, QuestionOption


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'options']


class QuestionWriteSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'order', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        for opt in options_data:
            QuestionOption.objects.create(question=question, **opt)
        return question


class TestResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'student', 'student_name', 'score', 'submitted_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class TestSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    result_count = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'group', 'group_name', 'total_questions',
                  'max_score', 'result_count', 'avg_score', 'question_count', 'created_at']

    def get_group_name(self, obj):
        return obj.group.name if obj.group else None

    def get_result_count(self, obj):
        return obj.results.count()

    def get_avg_score(self, obj):
        results = obj.results.all()
        if not results.exists():
            return 0
        return round(sum(r.score for r in results) / results.count(), 1)

    def get_question_count(self, obj):
        return obj.questions.count()


class TestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['title', 'group', 'total_questions', 'max_score']


class TestSubmitSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    score = serializers.IntegerField()

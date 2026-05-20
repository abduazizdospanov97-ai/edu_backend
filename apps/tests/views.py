from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Test, TestResult, Question
from .serializers import (
    TestSerializer, TestWriteSerializer, TestSubmitSerializer,
    TestResultSerializer, QuestionSerializer, QuestionWriteSerializer,
)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.select_related('group').prefetch_related('results', 'questions').order_by('-created_at')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TestWriteSerializer
        return TestSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        group_id = request.query_params.get('group_id')
        if group_id:
            qs = qs.filter(group_id=group_id)
        return Response({'success': True, 'data': TestSerializer(qs, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({'success': True, 'data': TestSerializer(obj).data})

    def create(self, request, *args, **kwargs):
        serializer = TestWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'success': True, 'data': TestSerializer(obj).data}, status=201)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({'success': True})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        test = self.get_object()
        serializer = TestSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result, _ = TestResult.objects.update_or_create(
            test=test,
            student_id=serializer.validated_data['student_id'],
            defaults={'score': serializer.validated_data['score']}
        )
        return Response({'success': True, 'data': TestResultSerializer(result).data})

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        test = self.get_object()
        results = test.results.select_related('student').order_by('-score')
        return Response({'success': True, 'data': TestResultSerializer(results, many=True).data})

    @action(detail=True, methods=['get', 'post'])
    def questions(self, request, pk=None):
        test = self.get_object()
        if request.method == 'GET':
            qs = test.questions.prefetch_related('options').order_by('order')
            return Response({'success': True, 'data': QuestionSerializer(qs, many=True).data})
        serializer = QuestionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save(test=test)
        return Response({'success': True, 'data': QuestionSerializer(question).data}, status=201)

    @action(detail=True, methods=['delete'], url_path=r'questions/(?P<question_id>\d+)')
    def delete_question(self, request, pk=None, question_id=None):
        test = self.get_object()
        try:
            question = test.questions.get(id=question_id)
            question.delete()
            return Response({'success': True})
        except Question.DoesNotExist:
            return Response({'success': False, 'error': 'Savol topilmadi'}, status=404)

from django.db import models
from apps.groups.models import Group
from apps.students.models import Student


class Test(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    max_score = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.test.title} — {self.text[:50]}"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.text}"


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('test', 'student')
        ordering = ['-score']

    def __str__(self):
        return f"{self.student} — {self.test} — {self.score}"

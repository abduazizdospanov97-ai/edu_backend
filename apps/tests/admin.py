from django.contrib import admin
from .models import Test, TestResult, Question, QuestionOption

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'total_questions', 'max_score', 'created_at']
    list_filter = ['group']
    search_fields = ['title']
    inlines = [QuestionInline]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'student', 'score', 'submitted_at']
    list_filter = ['test']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'text', 'order']
    inlines = [QuestionOptionInline]

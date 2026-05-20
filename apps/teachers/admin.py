from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'phone', 'salary']
    search_fields = ['user__name', 'subject', 'phone']

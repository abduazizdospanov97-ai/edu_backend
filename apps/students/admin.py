from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'course', 'group', 'balance', 'status']
    list_filter = ['status', 'course', 'group']
    search_fields = ['first_name', 'last_name', 'phone']
    ordering = ['first_name', 'last_name']

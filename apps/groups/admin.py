from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'teacher', 'room', 'max_students']
    list_filter = ['course', 'teacher']
    search_fields = ['name']

from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'date', 'status']
    list_filter = ['status', 'group', 'date']
    search_fields = ['student__first_name', 'student__last_name']
    date_hierarchy = 'date'

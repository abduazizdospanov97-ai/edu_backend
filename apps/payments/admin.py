from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'method', 'status', 'created_at']
    list_filter = ['method', 'status']
    search_fields = ['student__first_name', 'student__last_name']
    date_hierarchy = 'created_at'

from django.db import models


class Payment(models.Model):
    METHOD_CHOICES = [
        ('CASH', 'Naqd'),
        ('CARD', 'Karta'),
        ('TRANSFER', "O'tkazma"),
    ]
    STATUS_CHOICES = [
        ('PAID', "To'langan"),
        ('PENDING', 'Kutilmoqda'),
    ]
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='CASH')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PAID')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} — {self.amount} so'm"

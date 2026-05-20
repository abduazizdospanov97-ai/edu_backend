from django.db import models


class Student(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Faol'),
        ('INACTIVE', 'Nofaol'),
        ('GRADUATED', 'Bitirgan'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

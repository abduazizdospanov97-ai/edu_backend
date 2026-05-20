from django.db import models


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Keldi'),
        ('ABSENT', 'Kelmadi'),
        ('LATE', 'Kech keldi'),
    ]
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')

    class Meta:
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'
        unique_together = ('student', 'group', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} — {self.date} — {self.status}"

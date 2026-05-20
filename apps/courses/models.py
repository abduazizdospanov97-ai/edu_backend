from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(default=6)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    color = models.CharField(max_length=20, default='#3B82F6')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['name']

    def __str__(self):
        return self.name

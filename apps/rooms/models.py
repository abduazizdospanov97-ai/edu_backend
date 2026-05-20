from django.db import models


class Room(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Bo\'sh'),
        ('OCCUPIED', 'Band'),
        ('MAINTENANCE', 'Ta\'mirda'),
    ]
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=20)
    floor = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    class Meta:
        verbose_name = 'Xona'
        verbose_name_plural = 'Xonalar'
        ordering = ['name']

    def __str__(self):
        return self.name

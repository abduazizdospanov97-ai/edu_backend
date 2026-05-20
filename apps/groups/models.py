from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey('rooms.Room', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    days = models.JSONField(default=list)
    max_students = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'
        ordering = ['name']

    def __str__(self):
        return self.name

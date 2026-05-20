from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='teacher_profile')
    phone = models.CharField(max_length=20, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subject = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"

    def __str__(self):
        return self.user.name

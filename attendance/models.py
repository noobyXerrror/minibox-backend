from django.db import models
from users.models import User  # or from employee.models import Employee if separated

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('IN', 'Check In'),
        ('OUT', 'Check Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.status} at {self.timestamp}"

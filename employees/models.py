from django.db import models
from django.conf import settings

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )
    phone = models.CharField(max_length=15, blank=True)
    position = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)

    def __str__(self):
        return f"{self.user.name} - {self.position}"

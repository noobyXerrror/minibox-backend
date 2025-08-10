from django.db import models
from employees.models import Employee

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # e.g. '2025-08'
    days_present = models.IntegerField()
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month')

    def __str__(self):
        return f"{self.employee.name} - {self.month}"

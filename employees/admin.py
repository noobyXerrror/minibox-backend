from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'position', 'date_joined', 'is_active', 'monthly_salary')
    list_filter = ('is_active', 'position')
    search_fields = ('user__email', 'user__name', 'position')
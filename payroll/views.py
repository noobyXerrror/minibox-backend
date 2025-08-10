from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from attendance.models import Attendance
from .models import Payroll
from .serializers import PayrollSerializer
from django.db.models import Q
from calendar import monthrange
from rest_framework.permissions import IsAuthenticated

class GeneratePayrollView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.role != 'HR' and request.user.role != 'ADMIN':
          return Response({"error": "Unauthorized"}, status=403)
    

        month = request.data.get('month')  # e.g., '2025-08'
        if not month:
            return Response({'error': 'Month is required in format YYYY-MM'}, status=400)

        employees = Employee.objects.all()
        report = []

        for emp in employees:
            days_present = Attendance.objects.filter(
                user=emp.user,
                timestamp__month=int(month.split('-')[1]),
                timestamp__year=int(month.split('-')[0])
            ).dates('timestamp', 'day').count()

            total_days = monthrange(int(month.split('-')[0]), int(month.split('-')[1]))[1]
            per_day_salary = emp.monthly_salary / total_days
            calculated_salary = round(per_day_salary * days_present, 2)

            payroll_obj, created = Payroll.objects.update_or_create(
                employee=emp,
                month=month,
                defaults={
                    'days_present': days_present,
                    'total_salary': calculated_salary
                }
            )
            report.append(PayrollSerializer(payroll_obj).data)

        return Response(report, status=201)

class PayrollReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        employee_id = request.query_params.get('employee')

        filters = Q()
        if month:
            filters &= Q(month=month)
        if employee_id:
            filters &= Q(employee__id=employee_id)

        queryset = Payroll.objects.filter(filters)
        serializer = PayrollSerializer(queryset, many=True)
        return Response(serializer.data)
